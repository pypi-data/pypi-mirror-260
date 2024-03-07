def comprehensiveness(pred: float, pred_no_rationale: float) -> float:
    r"""Calculate the comprehensiveness of a explanation.

    comprehensiveness = m(x_i)_j - m(x_i \ r_i)_j, where m(x_i)_j is the original model's prediction for the j-th class
    and m(x_i \ r_i)_j is the model's prediction for the j-th class after removing the i-th explanation.

    A high score here implies that the rationales were indeed influential in the prediction, while a low score suggests
    that they were not.

    Args:
        pred (float): The model's prediction for the original input.
        pred_no_rationale (float): The model's prediction for the input after removing the rationale.

    Returns:
        float: The comprehensiveness score.
    """
    return pred - pred_no_rationale


def sufficiency(pred: float, pred_rationale_only: float) -> float:
    r"""Calculate the sufficiency of a explanation.

    sufficiency = m(x_i)_j - m(r_i)_j, where m(x_i)_j is the original model's prediction for the j-th class
    and m(r_i)_j is the model's prediction for the j-th class after adding the i-th explanation.

    This captures the degree to which the snippets within the extracted rationales are adequate for a model to make a prediction.

    Args:
        pred (float): The model's prediction for the original input.
        pred_rationale_only (float): The model's prediction for the input after adding the rationale.

    Returns:
        float: The sufficiency score.
    """
    return pred - pred_rationale_only
