from scipy.stats import chi2_contingency


def test_for_sample_ratio_mismatch(
    control_group1_size,
    control_group2_size,
    variant_group1_size,
    variant_group2_size,
    alpha=0.05,
):

    table = [
        [control_group1_size, control_group2_size],
        [variant_group1_size, variant_group2_size],
    ]
    stat, p_value, dof, expected = chi2_contingency(table, correction=False)

    decision = "Discard A/B test results" if p_value <= alpha else "Don't discard A/B test results"

    return {
        "P-value": round(p_value, 5),
        "Alpha value (significance level)": alpha,
        "Decision": decision,
    }
