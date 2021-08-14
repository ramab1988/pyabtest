from scipy.stats import chi2_contingency


def test_for_binary_metric(
    control_success, control_failures, variant_success, variant_failures, alpha=0.05
):

    table = [[control_success, control_failures], [variant_success, variant_failures]]
    stat, p_value, dof, expected = chi2_contingency(table, correction=False)

    decision = (
        "Reject null hypothesis"
        if p_value <= alpha
        else "Do not reject null hypothesis"
    )

    return {
        "P-value": round(p_value, 5),
        "Alpha value (significance level)": alpha,
        "Decision": decision,
    }


def test_for_sample_ratio_mismatch(
    control_success, control_failures, variant_success, variant_failures, alpha=0.05
):
    result = test_for_binary_metric(
        control_success, control_failures, variant_success, variant_failures, alpha
    )
    if result["Decision"] == "Reject null hypothesis":
        decision = "Discard A/B test results"
    else:
        decision = "Don't discard A/B test results"
    result["Decision"] = decision
    return result
