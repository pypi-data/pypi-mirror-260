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
from span_explain.lime.index_string import IndexedCharacters, IndexedString


class TextDomainMapper(explanation.DomainMapper):
    """Maps feature ids to words or word-positions"""

    def __init__(self, indexed_string: IndexedString) -> None:
        """Initializer.

        Args:
            indexed_string: lime_text.IndexedString, original string
        """
        self.indexed_string = indexed_string

    def map_exp_ids(self, exp: list[tuple[int, float]], positions: bool = False) -> list[tuple[str, float]]:
        """Maps ids to words or word-position strings.

        Args:
            exp: list of tuples [(id, weight), (id,weight)]
            positions: if True, also return word positions

        Returns:
            list of tuples (word, weight), or (word_positions, weight) if
            examples: ('bad', 1) or ('bad_3-6-12', 1)
        """
        if positions:
            exp = [
                (
                    f"{self.indexed_string.word(x[0])}_\
                    {'-'.join(map(str, self.indexed_string.string_position(x[0])))}",
                    x[1],
                )
                for x in exp
            ]
        else:
            exp = [(self.indexed_string.word(x[0]), x[1]) for x in exp]
        return exp

    def visualize_instance_html(
        self,
        exp: list[tuple[str, float]],
        label: int,
        div_name: str,
        exp_object_name: str,
        text: bool = True,
        opacity: bool = True,
    ) -> str:
        """Adds text with highlighted words to visualization.

        Args:
            exp: list of tuples [(id, weight), (id,weight)]
            label: label id (integer)
            div_name: name of div object to be used for rendering(in js)
            exp_object_name: name of js explanation object
            text: if False, return empty
            opacity: if True, fade colors according to weight
        """
        if not text:
            return ""
        text = self.indexed_string.raw_string().encode("utf-8", "xmlcharrefreplace").decode("utf-8")
        text = re.sub(r"[<>&]", "|", text)
        exp = [
            (
                self.indexed_string.word(x[0]),
                self.indexed_string.string_position(x[0]),
                x[1],
            )
            for x in exp
        ]

        all_occurrences = list(itertools.chain.from_iterable([itertools.product([x[0]], x[1], [x[2]]) for x in exp]))
        all_occurrences = [(x[0], int(x[1]), x[2]) for x in all_occurrences]

        return f"""
            {exp_object_name}.show_raw_text({json.dumps(all_occurrences)}, {label}, {json.dumps(text)}, \
            {div_name}, {json.dumps(opacity)});
            """


class LimeTextExplainer:
    """Explains text classifiers.
    Currently, we are using an exponential kernel on cosine distance, and
    restricting explanations to words that are present in documents.
    """

    def __init__(
        self,
        kernel_width: int = 25,
        kernel=None,
        verbose: bool = False,
        class_names: list[str] | None = None,
        feature_selection: str = "auto",
        split_expression: str = r"\W+",
        bow: bool = True,
        mask_string=None,
        random_state=None,
        char_level=False,
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
            split_expression: Regex string or callable. If regex string, will be used with re.split.
                If callable, the function should return a list of tokens.
            bow: if True (bag of words), will perturb input data by removing
                all occurrences of individual words or characters.
                Explanations will be in terms of these words. Otherwise, will
                explain in terms of word-positions, so that a word may be
                important the first time it appears and unimportant the second.
                Only set to false if the classifier uses word order in some way
                (bigrams, etc), or if you set char_level=True.
            mask_string: String used to mask tokens or characters if bow=False
                if None, will be 'UNKWORDZ' if char_level=False, chr(0)
                otherwise.
            random_state: an integer or numpy.RandomState that will be used to
                generate random numbers. If None, the random state will be
                initialized using the internal numpy seed.
            char_level: an boolean identifying that we treat each character
                as an independent occurence in the string
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
        self.bow = bow
        self.mask_string = mask_string
        self.split_expression = split_expression
        self.char_level = char_level

    def explain_instance(
        self,
        text_instance: str,
        classifier_fn: callable,
        labels=(1,),
        top_labels: int | None = None,
        num_features: int = 10,
        num_samples: int = 5000,
        distance_metric: str = "cosine",
        model_regressor: object | None = None,
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

        Returns:
            An Explanation object (see explanation.py) with the corresponding
            explanations.
        """
        indexed_string = (
            IndexedCharacters(text_instance, bow=self.bow, mask_string=self.mask_string)
            if self.char_level
            else IndexedString(
                text_instance,
                bow=self.bow,
                split_expression=self.split_expression,
                mask_string=self.mask_string,
            )
        )

        domain_mapper = TextDomainMapper(indexed_string)
        data, yss, distances = self.__data_labels_distances(
            indexed_string,
            classifier_fn,
            num_samples,
            distance_metric=distance_metric,
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

    def sample_perturbations(
        self,
        indexed_string: IndexedString,
        num_samples: int,
        k: int,
    ) -> tuple[np.ndarray, list[str]]:
        """Sample a number of perturbations.

        Note: The first perturbation is always the original input.

        Args:
            indexed_string: document (IndexedString) to be explained,
            num_samples: size of the neighborhood to learn the linear model
            k: number of words in the document

        Returns:
            A tuple (data, inverse_data), where:
                data: dense num_samples * K binary matrix, where K is the
                    number of tokens in indexed_string. The first row is the
                    original instance, and thus a row of ones.
                inverse_data: list of strings, where each string is the
                    original string with some words removed.
        """
        sample = self.random_state.randint(1, k + 1, num_samples - 1)
        data = np.ones((num_samples, k))
        data[0] = np.ones(k)
        features_range = range(k)
        inverse_data = [indexed_string.raw_string()]
        for i, size in enumerate(sample, start=1):
            inactive = self.random_state.choice(features_range, size, replace=False)
            data[i, inactive] = 0
            inverse_data.append(indexed_string.inverse_removing(inactive))

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
        indexed_string: IndexedString,
        classifier_fn: callable,
        num_samples: int,
        distance_metric: str = "cosine",
    ):
        """Generates a neighborhood around a prediction.

        Generates neighborhood data by randomly removing words from
        the instance, and predicting with the classifier. Uses cosine distance
        to compute distances between original and perturbed instances.

        Args:
            indexed_string: document (IndexedString) to be explained,
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
        k = indexed_string.num_words()
        data, perturbations = self.sample_perturbations(indexed_string, num_samples, k)

        # Predict with classifier
        labels = classifier_fn(perturbations)

        # Compute distances to the original instance
        distances = self.compute_distances(sp.sparse.csr_matrix(data), distance_metric)

        return data, labels, distances
