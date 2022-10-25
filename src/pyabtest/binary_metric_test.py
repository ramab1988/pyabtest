from scipy.stats import chi2_contingency


def test_for_binary_metric(control_success, control_failures, variant_success, variant_failures, alpha=0.05):

    table = [[control_success, control_failures], [variant_success, variant_failures]]
    stat, p_value, dof, expected = chi2_contingency(table, correction=False)

    decision = "Reject null hypothesis" if p_value <= alpha else "Do not reject null hypothesis"

    return {
        "P-value": round(p_value, 5),
        "Alpha value (significance level)": alpha,
        "Decision": decision,
    }
