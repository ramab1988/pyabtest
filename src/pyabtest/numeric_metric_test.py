import numpy as np
from sklearn.utils import resample
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from numpy import random
from numba import jit
from scipy.stats import t
import warnings

warnings.filterwarnings("ignore")


def get_bootstrapped_data(params):

    data, length, random_number = params
    sample = resample(data, n_samples=length, random_state=random_number)
    return np.mean(sample)


def bootstrap_test_old(control_observations, variant_observations, alpha=0.05, no_of_samples=10000):

    thread_pool = cpu_count()
    combined = np.concatenate((control_observations, variant_observations), axis=0)

    bootstrap_control = []
    bootstrap_variant = []

    for i in range(no_of_samples):
        bootstrap_control.append((combined, len(control_observations), np.random.randint(i + 1)))
        bootstrap_variant.append((combined, len(variant_observations), np.random.randint(i + 1)))

    pool = ThreadPool(thread_pool)
    bootstrap_control_mean = np.array(pool.map(get_bootstrapped_data, bootstrap_control))
    pool.close()
    pool.join()

    pool = ThreadPool(thread_pool)
    bootstrap_variant_mean = np.array(pool.map(get_bootstrapped_data, bootstrap_variant))
    pool.close()
    pool.join()

    dif_bootstrap_means = bootstrap_control_mean - bootstrap_variant_mean

    obs_difs = np.mean(control_observations) - np.mean(variant_observations)

    p_value = dif_bootstrap_means[dif_bootstrap_means >= obs_difs].shape[0] / no_of_samples

    decision = "Reject null hypothesis" if p_value <= alpha else "Do not reject null hypothesis"

    return {
        "P-value": round(p_value, 5),
        "Alpha value (significance level)": alpha,
        "Decision": decision,
    }


@jit(nopython=True, parallel=True, fastmath=True)
def compute_test_statistic(control_observations, variant_observations):
    return (np.mean(control_observations) - np.mean(variant_observations)) / np.sqrt(
        np.var(control_observations) / control_observations.size
        + np.var(variant_observations) / variant_observations.size
    )


@jit(nopython=True, parallel=True, fastmath=True)
def compute_bootstrap_statistic(control_new_observations, variant_new_observations, no_of_samples):
    bootstrap_statistics = []
    for _ in range(no_of_samples):
        bootstrap_statistics.append(
            compute_test_statistic(
                np.random.choice(
                    control_new_observations,
                    replace=True,
                    size=control_new_observations.size,
                ),
                np.random.choice(
                    variant_new_observations,
                    replace=True,
                    size=variant_new_observations.size,
                ),
            )
        )
    return np.array(bootstrap_statistics)


def bootstrap_test_new(control_observations, variant_observations, alpha=0.05, no_of_samples=10000):

    control_observations = np.array(control_observations)
    variant_observations = np.array(variant_observations)

    test_statistic = compute_test_statistic(control_observations, variant_observations)

    combined_observations = np.concatenate((control_observations, variant_observations), axis=0)
    combined_mean = np.mean(combined_observations)

    control_new_observations = control_observations - np.mean(control_observations) + combined_mean
    variant_new_observations = variant_observations - np.mean(variant_observations) + combined_mean

    bootstrap_statistics = compute_bootstrap_statistic(
        control_new_observations, variant_new_observations, no_of_samples
    )

    p_value = (bootstrap_statistics >= test_statistic).size / no_of_samples

    decision = "Reject null hypothesis" if p_value <= alpha else "Do not reject null hypothesis"

    return {
        "P-value": round(p_value, 5),
        "Alpha value (significance level)": alpha,
        "Decision": decision,
    }


def welch_ttest(control_observations, variant_observations, alpha=0.05):

    control_observations = np.array(control_observations)
    variant_observations = np.array(variant_observations)

    n_x = len(control_observations)
    n_y = len(variant_observations)

    s_x = np.sqrt(np.var(control_observations, ddof=1))
    s_y = np.sqrt(np.var(variant_observations, ddof=1))

    s_d = np.sqrt(s_x**2 / n_x + s_y**2 / n_y)

    dofs = s_d**4 / ((s_x**2 / n_x) ** 2 / (n_x - 1) + (s_y**2 / n_y) ** 2 / (n_y - 1))
    stat_distrib = t(df=dofs, loc=0, scale=1)

    t_val = (control_observations.mean() - variant_observations.mean()) / s_d

    p_value = stat_distrib.cdf(t_val) * 2

    decision = "Reject null hypothesis" if p_value <= alpha else "Do not reject null hypothesis"

    return {
        "P-value": round(p_value, 5),
        "Alpha value (significance level)": alpha,
        "Decision": decision,
    }


def test_for_numeric_metric(control_observations, variant_observations, test_type="ttest", alpha=0.05):
    if test_type == "ttest":
        return welch_ttest(control_observations, variant_observations, alpha)
    else:
        return bootstrap_test_old(control_observations, variant_observations, alpha)
