from numpy import random
import numpy as np
from numba import jit
import warnings
warnings.filterwarnings('ignore')


@jit(nopython=True, parallel=True, fastmath=True)
def compute_test_statistic(control_observations, variant_observations):
    return (np.mean(control_observations) - np.mean(variant_observations)) / np.sqrt(
        np.var(control_observations) / control_observations.size
        + np.var(variant_observations) / variant_observations.size
    )


@jit(nopython=True, parallel=True, fastmath=True)
def compute_bootstrap_statistic(
    control_new_observations, variant_new_observations, no_of_samples
):
    bootstrap_statistics = []
    for _ in range(no_of_samples):
        bootstrap_statistics.append(
            compute_test_statistic(
                np.random.choice(
                    control_new_observations,
                    replace=True,
                    size=len(control_new_observations),
                ),
                np.random.choice(
                    variant_new_observations,
                    replace=True,
                    size=len(variant_new_observations),
                ),
            )
        )
    return np.array(bootstrap_statistics)


def test_for_numeric_metric(
    control_observations, variant_observations, alpha=0.05, no_of_samples=10000
):

    control_observations = np.array(control_observations)
    variant_observations = np.array(variant_observations)

    test_statistic = compute_test_statistic(control_observations, variant_observations)

    combined_observations = np.concatenate(
        (control_observations, variant_observations), axis=0
    )
    combined_mean = np.mean(combined_observations)

    control_new_observations = (
        control_observations - np.mean(control_observations) + combined_mean
    )
    variant_new_observations = (
        variant_observations - np.mean(variant_observations) + combined_mean
    )

    bootstrap_statistics = compute_bootstrap_statistic(
        control_new_observations, variant_new_observations, no_of_samples
    )

    p_value = (bootstrap_statistics >= test_statistic).size / no_of_samples

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

