"""
Functions for explaining text classifiers.
"""

from __future__ import annotations

import itertools
import json
import re
from functools import partial

import numpy as np
import scipy as sp
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.utils import check_random_state

from span_explain.lime import explanation, lime_base
from span_explain.lime.index_spans import IndexedSpans


class SpanDomainMapper(explanation.DomainMapper):
    """Maps feature ids to words or word-positions"""

    def __init__(self, indexed_spans: IndexedSpans):
        """Initializer.

        Args:
            indexed_spans: IndexedSpans object to be mapped
        """
        self.indexed_spans = indexed_spans

    def map_exp_ids(self, exp: list[tuple[int, float]], positions: bool = False) -> list[tuple[str, float]]:
        """Maps ids to spans or span-position strings.

        Args:
            exp: list of tuples [(id, weight), (id, weight)]
            positions: if True, also return span positions

        Returns:
            list of tuples (span, weight), or (span_positions, weight) if positions=True
            Examples: ('The quick brown fox...', 1) or ('Span_0-15', 1) if positions=True
        """
        return [(self.indexed_spans.span(span_idx), weight) for span_idx, weight in exp]

    def visualize_instance_html(
        self,
        exp: list[tuple[int, float]],
        label: int,
        div_name: str,
        exp_object_name: str,
        text: bool = True,
        opacity: bool = True,
    ) -> str:
        """Adds text with highlighted spans to visualization.

        Args:
            exp: list of tuples [(id, weight), (id, weight)]
            label: label id (integer)
            div_name: name of div object to be used for rendering (in js)
            exp_object_name: name of js explanation object
            text: if False, return empty
            opacity: if True, fade colors according to weight
        """
        if not text:
            return ""

        text = self.indexed_spans.raw_string().encode("utf-8", "xmlcharrefreplace").decode("utf-8")
        text = re.sub(r"[<>&]", "|", text)

        exp = [
            (
                self.indexed_spans.span(span_idx),
                self.indexed_spans.get_span_start(span_idx),
                weight,
            )
            for span_idx, weight in exp
        ]
        all_occurrences = list(itertools.chain.from_iterable([itertools.product([x[0]], x[1], [x[2]]) for x in exp]))
        all_occurrences = [(x[0], int(x[1]), x[2]) for x in all_occurrences]

        return f"""
            {exp_object_name}.show_raw_text({json.dumps(all_occurrences)}, {label}, {json.dumps(text)}, \
            {div_name}, {json.dumps(opacity)});
            """


class LimeSpansExplainer:
    """Explains text classifiers using spans (sentences) as features."""

    def __init__(
        self,
        kernel_width: int = 25,
        kernel=None,
        verbose: bool = False,
        class_names: list[str] | None = None,
        feature_selection: str = "auto",
        random_state: int | None = None,
        show_spans: bool = False,
    ):
        """Init function.

        Args:
            kernel_width: kernel width for the exponential kernel.
            kernel: similarity kernel that takes euclidean distances and kernel
                width as input and outputs weights in (0,1). If None, defaults to
                an exponential kernel.
            verbose: if true, print local prediction values from linear model
            class_names: list of class names, ordered according to whatever the
                classifier is using. If not present, class names will be '0',
                '1', ...
            feature_selection: feature selection method. can be
                'forward_selection', 'lasso_path', 'none' or 'auto'.
                See function 'explain_instance_with_data' in lime_base.py for
                details on what each of the options does.
            random_state: an integer or numpy.RandomState that will be used to
                generate random numbers. If None, the random state will be
                initialized using the internal numpy seed.
            show_spans: if True, show spans in the explanation. Default is False.
        """
        if kernel is None:

            def kernel(distances: np.ndarray, kernel_width: int) -> np.ndarray:
                """Exponential kernel

                K(distances) = exp(-distances^2 / kernel_width^2)
                """
                return np.sqrt(np.exp(-(distances**2) / kernel_width**2))

        kernel_fn = partial(kernel, kernel_width=kernel_width)

        self.random_state = check_random_state(random_state)
        self.base = lime_base.LimeBase(kernel_fn, verbose, random_state=self.random_state)
        self.class_names = class_names
        self.vocabulary = None
        self.feature_selection = feature_selection
        self.show_spans = show_spans

    def explain_instance(
        self,
        text_instance: str,
        classifier_fn: callable,
        labels: list[int] | None = (1,),
        top_labels: int | None = None,
        num_features: int = 10,
        num_samples: int = 5000,
        distance_metric: str = "cosine",
        model_regressor: object | None = None,
        spans: list[str] | None = None,
        span_extractor_fn: callable | None = None,
        **kwargs,
    ):
        """Generates explanations for a prediction.

        First, we generate neighborhood data by randomly hiding features from
        the instance (see __data_labels_distance_mapping). We then learn
        locally weighted linear models on this neighborhood data to explain
        each of the classes in an interpretable way (see lime_base.py).

        Args:
            text_instance: raw text string to be explained.
            classifier_fn: classifier prediction probability function, which
                takes a list of d strings and outputs a (d, k) numpy array with
                prediction probabilities, where k is the number of classes.
                For ScikitClassifiers , this is classifier.predict_proba.
            labels: iterable with labels to be explained.
            top_labels: if not None, ignore labels and produce explanations for
                the K labels with highest prediction probabilities, where K is
                this parameter.
            num_features: maximum number of features present in explanation
            num_samples: size of the neighborhood to learn the linear model
            distance_metric: the distance metric to use for sample weighting,
                defaults to cosine similarity
            model_regressor: sklearn regressor to use in explanation. Defaults
            to Ridge regression in LimeBase. Must have model_regressor.coef_
            and 'sample_weight' as a parameter to model_regressor.fit()
            spans (list[str] | None): A list of strings, each representing an important
                span (sentence) from the raw_string. If None, then the span_extractor_fn
                must be provided.
            span_extractor_fn (callable | None): A function that extracts spans from the
                raw string. If None, then the spans must be provided.

        Returns:
            An Explanation object (see explanation.py) with the corresponding
            explanations.
        """
        indexed_spans = IndexedSpans(
            text_instance,
            spans=spans,
            span_extractor_fn=span_extractor_fn,
        )
        if self.show_spans:
            print(f"{indexed_spans.spans=}")

        domain_mapper = SpanDomainMapper(indexed_spans)
        data, yss, distances = self.__data_labels_distances(
            indexed_spans,
            classifier_fn,
            num_samples,
            distance_metric,
        )

        if self.class_names is None:
            self.class_names = [str(x) for x in range(yss[0].shape[0])]

        ret_exp = explanation.Explanation(
            domain_mapper=domain_mapper,
            class_names=self.class_names,
            random_state=self.random_state,
        )
        ret_exp.predict_proba = yss[0]  # The prediction probability of the original instance

        if top_labels:
            # Only create explanations for the K labels with highest prediction probabilities
            labels = np.argsort(yss[0])[-top_labels:]
            ret_exp.top_labels = list(labels)
            ret_exp.top_labels.reverse()

        for label in labels:
            (
                ret_exp.intercept[label],
                ret_exp.local_exp[label],
                ret_exp.score[label],
                ret_exp.local_pred[label],
            ) = self.base.explain_instance_with_data(
                data,
                yss,
                distances,
                label,
                num_features,
                model_regressor=model_regressor,
                feature_selection=self.feature_selection,
            )

        return ret_exp

    def sample_perturbations(self, indexed_spans: IndexedSpans, num_samples: int) -> tuple[np.ndarray, list[str]]:
        """Sample a number of perturbations.

        Note: The first perturbation is always the original input.

        Args:
            indexed_string: document (IndexedSpans) to be explained,
            num_samples: size of the neighborhood to learn the linear model

        Returns:
            A tuple (data, inverse_data), where:
                data: dense num_samples * K binary matrix, where K is the
                    number of tokens in indexed_string. The first row is the
                    original instance, and thus a row of ones.
                inverse_data: list of strings, where each string is the
                    original string with some spans removed.
        """
        k = indexed_spans.num_spans()

        # Get a random number of spans to remove
        sample = self.random_state.randint(1, k + 1, num_samples - 1)

        # Generate data by randomly removing spans from the instance
        data = np.ones((num_samples, k))
        data[0] = np.ones(k)
        features_range = range(k)
        inverse_data = [indexed_spans.raw_string()]
        for i, size in enumerate(sample, start=1):
            inactive = self.random_state.choice(features_range, size, replace=False)
            data[i, inactive] = 0
            inverse_data.append(indexed_spans.inverse_removing(inactive))

        return data, inverse_data

    def compute_distances(self, perturbations: np.ndarray, distance_metric: str = "cosine") -> np.ndarray:
        """Computes distances between perturbations and original instance.

        Args:
            perturbations: sparse matrix with perturbations.
            distance_metric: the distance metric to use for sample weighting,
                defaults to cosine similarity.

        Returns:
            distances: distances between perturbations and original instance.
        """
        original_data = perturbations[0]
        distances = pairwise_distances(
            X=perturbations,
            Y=original_data,
            metric=distance_metric,
        )

        return distances.ravel() * 100

    def __data_labels_distances(
        self,
        indexed_spans: IndexedSpans,
        classifier_fn: callable,
        num_samples: int,
        distance_metric: str = "cosine",
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Generates a neighborhood around a prediction.

        Generates neighborhood data by randomly removing spans from
        the instance, and predicting with the classifier. Uses cosine distance
        to compute distances between original and perturbed instances.

        Args:
            indexed_string: document (IndexedSpans) to be explained,
            classifier_fn: classifier prediction probability function, which
                takes a string and outputs prediction probabilities. For
                ScikitClassifier, this is classifier.predict_proba.
            num_samples: size of the neighborhood to learn the linear model
            distance_metric: the distance metric to use for sample weighting,
                defaults to cosine similarity.

        Returns:
            A tuple (data, labels, distances), where:
                data: dense num_samples * K binary matrix, where K is the
                    number of tokens in indexed_string. The first row is the
                    original instance, and thus a row of ones.
                labels: num_samples * L matrix, where L is the number of target
                    labels
                distances: cosine distance between the original instance and
                    each perturbed instance (computed in the binary 'data'
                    matrix), times 100.
        """
        # Generate neighborhood data
        data, perturbations = self.sample_perturbations(indexed_spans, num_samples)

        # Predict with classifier
        labels = classifier_fn(perturbations)

        # Compute distances to the original instance
        distances = self.compute_distances(sp.sparse.csr_matrix(data), distance_metric)

        return data, labels, distances
