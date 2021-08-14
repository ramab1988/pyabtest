import numpy as np
from scipy.stats import t


def welch_ttest(control_observations, variant_observations, alpha=0.05):

    control_observations = np.array(control_observations)
    variant_observations = np.array(variant_observations)

    n_x = len(control_observations)
    n_y = len(variant_observations)

    s_x = np.sqrt(np.var(control_observations, ddof=1))
    s_y = np.sqrt(np.var(variant_observations, ddof=1))

    s_d = np.sqrt(s_x ** 2 / n_x + s_y ** 2 / n_y)

    dofs = s_d ** 4 / (
        (s_x ** 2 / n_x) ** 2 / (n_x - 1) + (s_y ** 2 / n_y) ** 2 / (n_y - 1)
    )
    stat_distrib = t(df=dofs, loc=0, scale=1)

    t_val = (control_observations.mean() - variant_observations.mean()) / s_d

    p_value = stat_distrib.cdf(t_val) * 2

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
