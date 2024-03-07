"""
Explanation class, with visualization functions.
"""
from __future__ import annotations

import json
import re
import string
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.utils import check_random_state

from .exceptions import LimeError


def id_generator(size=15, random_state=None):
    """Helper function to generate random div ids. This is useful for embedding
    HTML into ipython notebooks."""
    chars = list(string.ascii_uppercase + string.digits)
    return "".join(random_state.choice(chars, size, replace=True))


class DomainMapper:
    """Class for mapping features to the specific domain.

    The idea is that there would be a subclass for each domain (text, tables,
    images, etc), so that we can have a general Explanation class, and separate
    out the specifics of visualizing features in here.
    """

    def __init__(self):
        pass

    def map_exp_ids(self, exp, **kwargs):
        """Maps the feature ids to concrete names.

        Default behaviour is the identity function. Subclasses can implement
        this as they see fit.

        Args:
            exp: list of tuples [(id, weight), (id,weight)]
            kwargs: optional keyword arguments

        Returns:
            exp: list of tuples [(name, weight), (name, weight)...]
        """
        return exp

    def visualize_instance_html(self, exp, label, div_name, exp_object_name, **kwargs):
        """Produces html for visualizing the instance.

        Default behaviour does nothing. Subclasses can implement this as they
        see fit.

        Args:
             exp: list of tuples [(id, weight), (id,weight)]
             label: label id (integer)
             div_name: name of div object to be used for rendering(in js)
             exp_object_name: name of js explanation object
             kwargs: optional keyword arguments

        Returns:
             js code for visualizing the instance
        """
        return ""


class Explanation:
    """Object returned by explainers."""

    def __init__(
        self,
        domain_mapper: DomainMapper,
        mode: str = "classification",
        class_names: list[str] | None = None,
        random_state: int | None = None,
    ) -> None:
        """Initializer.

        Args:
            domain_mapper: must inherit from DomainMapper class
            type: "classification" or "regression"
            class_names: list of class names (only used for classification)
            random_state: an integer or numpy.RandomState that will be used to
                generate random numbers. If None, the random state will be
                initialized using the internal numpy seed.
        """
        self.random_state = random_state
        self.mode = mode
        self.domain_mapper = domain_mapper
        self.local_exp = {}
        self.intercept = {}
        self.score = {}
        self.local_pred = {}
        if mode == "classification":
            self.class_names = class_names
            self.top_labels = None
            self.predict_proba = None
        elif mode == "regression":
            self.class_names = ["negative", "positive"]
            self.predicted_value = None
            self.min_value = 0.0
            self.max_value = 1.0
            self.dummy_label = 1
        else:
            error = f"Invalid explanation mode {mode}. Should be either 'classification' or 'regression'."
            raise LimeError(error)

    def available_labels(self) -> list[int]:
        """
        Returns the list of classification labels for which we have any explanations.
        """
        try:
            assert self.mode == "classification"
        except AssertionError as e:
            error = "Not supported for regression explanations."
            raise NotImplementedError(error) from e
        else:
            ans = self.top_labels if self.top_labels else self.local_exp.keys()
            return list(ans)

    def as_list(self, label: int = 1, **kwargs) -> list[tuple[str, float]]:
        """Returns the explanation as a list.

        Args:
            label: desired label. If you ask for a label for which an
                explanation wasn't computed, will throw an exception.
                Will be ignored for regression explanations.
            kwargs: keyword arguments, passed to domain_mapper

        Returns:
            list of tuples (representation, weight), where representation is
            given by domain_mapper. Weight is a float.
        """
        label_to_use = label if self.mode == "classification" else self.dummy_label
        ans = self.domain_mapper.map_exp_ids(self.local_exp[label_to_use], **kwargs)

        return [(x[0], float(x[1])) for x in ans]

    def as_map(self) -> dict[int, list[tuple[str, float]]]:
        """Returns the map of explanations.

        Returns:
            Map from label to list of tuples (feature_id, weight).
        """
        return self.local_exp

    def as_pyplot_figure(
        self,
        label: int = 1,
        normalize_weights: bool = True,
        base_height: float = 1,
        width: float = 10,
        wrap_length: int = 50,
        font_size: int = 8,
        **kwargs,
    ) -> plt.Figure:
        """Returns the explanation as a pyplot figure with optional normalization and fixed x-axis range."""
        exp = self.as_list(label=label, **kwargs)

        if normalize_weights:
            total_weight = sum([abs(x[1]) for x in exp])
            if total_weight > 0:
                exp = [(x[0], x[1] / total_weight) for x in exp]

        # Dynamically set the figure height based on the number of labels
        height = len(exp) * base_height
        fig = plt.figure(figsize=(width, height))
        vals = [x[1] for x in exp]
        names = [textwrap.fill(x[0], wrap_length) for x in exp]  # Wrap text
        vals.reverse()
        names.reverse()
        colors = ["green" if x > 0 else "red" for x in vals]
        pos = np.arange(len(exp)) + 0.5
        plt.barh(pos, vals, align="center", color=colors)
        plt.yticks(pos, names, fontsize=font_size)  # Set font size

        # Set x-axis limits
        plt.xlim(-1, 1)

        if self.mode == "classification":
            title = f"Local explanation for class {self.class_names[label]}"
        else:
            title = "Local explanation"
        plt.title(title)

        # Automatically adjust layout
        plt.tight_layout()

        return fig

    def show_in_notebook(
        self,
        labels: tuple[int] | None = None,
        predict_proba: bool = True,
        show_predicted_value: bool = True,
        dark_mode: bool = False,
        **kwargs,
    ):
        """Shows html explanation in ipython notebook.

        See as_html() for parameters.
        This will throw an error if you don't have IPython installed"""

        from IPython.core.display import HTML, display

        display(
            HTML(
                self.as_html(
                    labels=labels,
                    predict_proba=predict_proba,
                    show_predicted_value=show_predicted_value,
                    dark_mode=dark_mode,
                    **kwargs,
                ),
            ),
        )

    def save_to_file(
        self,
        file_path: str,
        labels: tuple[int] | None = None,
        predict_proba: bool = True,
        show_predicted_value: bool = True,
        **kwargs,
    ) -> None:
        """Saves html explanation to file. .

        Params:
            file_path: file to save explanations to

        See as_html() for additional parameters.
        """
        file_path = Path(file_path)
        file_ = file_path.open(file_path, "w", encoding="utf8")
        file_.write(
            self.as_html(
                labels=labels,
                predict_proba=predict_proba,
                show_predicted_value=show_predicted_value,
                **kwargs,
            ),
        )
        file_.close()

    def as_html(
        self,
        labels: tuple[int] | None = None,
        predict_proba: bool = True,
        show_predicted_value: bool = True,
        dark_mode: bool = False,
        **kwargs,
    ) -> str:
        """Returns the explanation as an html page.

        Args:
            labels: desired labels to show explanations for (as barcharts).
                If you ask for a label for which an explanation wasn't
                computed, will throw an exception. If None, will show
                explanations for all available labels. (only used for classification)
            predict_proba: if true, add  barchart with prediction probabilities
                for the top classes. (only used for classification)
            show_predicted_value: if true, add  barchart with expected value
                (only used for regression)
            dark_mode: if true, updates all text color to white in the resulting HTML
                (only useful when using show_in_notebook() from a notebook rendered
                in dark mode)
            kwargs: keyword arguments, passed to domain_mapper

        Returns:
            code for an html page, including javascript includes.
        """

        def jsonize(x: list[str]) -> str:
            return json.dumps(x, ensure_ascii=False)

        if labels is None and self.mode == "classification":
            labels = self.available_labels()

        this_dir = Path(__file__).parent
        bundle_path = this_dir / "bundle.js"
        with bundle_path.open(encoding="utf8") as file:
            bundle = file.read()

        out = f"""<html>
        <meta http-equiv="content-type" content="text/html; charset=UTF8">
        <head><script>{bundle} </script></head><body>"""
        random_id = id_generator(size=15, random_state=check_random_state(self.random_state))
        out += f"""
        <div class="lime top_div" id="top_div{random_id}"></div>
        """

        predict_proba_js = ""
        if self.mode == "classification" and predict_proba:
            predict_proba_js = f"""
            var pp_div = top_div.append('div')
                                .classed('lime predict_proba', true);
            var pp_svg = pp_div.append('svg').style('width', '100%%');
            var pp = new lime.PredictProba(pp_svg, \
            {jsonize([str(x) for x in self.class_names])}, {jsonize(list(self.predict_proba.astype(float)))});
            """

        predict_value_js = ""
        if self.mode == "regression" and show_predicted_value:
            predict_value_js = f"""
                var pp_div = top_div.append('div')
                                    .classed('lime predicted_value', true);
                var pp_svg = pp_div.append('svg').style('width', '100%%');
                var pp = new lime.PredictedValue(pp_svg, \
                {jsonize(float(self.predicted_value))}, {jsonize(float(self.min_value))}, \
                {jsonize(float(self.max_value))});
                """

        exp_js = f"""var exp_div;
            var exp = new lime.Explanation({jsonize([str(x) for x in self.class_names])});
        """

        if self.mode == "classification":
            for label in labels:
                exp = self.as_list(label)

                # Normalize to 1
                # total_weight = sum([abs(x[1]) for x in exp])
                # if total_weight > 0:
                #     exp = [(x[0], x[1] / total_weight) for x in exp]

                exp = jsonize(exp)
                exp_js += """
                exp_div = top_div.append('div').classed('lime explanation', true);
                exp.show(%s, %d, exp_div);
                """ % (exp, label)
        else:
            exp = jsonize(self.as_list())
            exp_js += f"""
            exp_div = top_div.append('div').classed('lime explanation', true);
            exp.show({exp}, {self.dummy_label}, exp_div);
            """

        raw_js = """var raw_div = top_div.append('div');"""

        html_data = self.local_exp[labels[0]] if self.mode == "classification" else self.local_exp[self.dummy_label]

        raw_js += self.domain_mapper.visualize_instance_html(
            exp=html_data,
            label=labels[0] if self.mode == "classification" else self.dummy_label,
            div_name="raw_div",
            exp_object_name="exp",
            **kwargs,
        )
        out += f"""
        <script>
        var top_div = d3.select('#top_div{random_id}').classed('lime top_div', true);
        {predict_proba_js}
        {predict_value_js}
        {exp_js}
        {raw_js}
        </script>
        """
        out += "</body></html>"

        if dark_mode:
            out = out.replace('"black"', '"#cccac3"')
            out = out.replace("all: initial;", "all: initial; color: #cccac3;")
            out = re.sub(r"svg.append\('text(((?!fill).)*);", r"svg.append('text\1.style('fill', '#cccac3');", out)

        return out
