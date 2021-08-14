import numpy as np
from sklearn.utils import resample
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count


def get_bootstrapped_data(params):

    data, length, random_number = params
    sample = resample(data, n_samples=length, random_state=random_number)
    return np.mean(sample)


def test_for_numeric_metric(
    control_observations, variant_observations, alpha=0.05, no_of_samples=10000
):

    thread_pool = cpu_count()
    combined = np.concatenate((control_observations, variant_observations), axis=0)

    bootstrap_control = []
    bootstrap_variant = []

    for i in range(no_of_samples):
        bootstrap_control.append(
            (combined, len(control_observations), np.random.randint(i + 1))
        )
        bootstrap_variant.append(
            (combined, len(variant_observations), np.random.randint(i + 1))
        )

    pool = ThreadPool(thread_pool)
    bootstrap_control_mean = np.array(
        pool.map(get_bootstrapped_data, bootstrap_control)
    )
    pool.close()
    pool.join()

    pool = ThreadPool(thread_pool)
    bootstrap_variant_mean = np.array(
        pool.map(get_bootstrapped_data, bootstrap_variant)
    )
    pool.close()
    pool.join()

    dif_bootstrap_means = bootstrap_control_mean - bootstrap_variant_mean

    obs_difs = np.mean(control_observations) - np.mean(variant_observations)

    p_value = (
        dif_bootstrap_means[dif_bootstrap_means >= obs_difs].shape[0] / no_of_samples
    )

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
