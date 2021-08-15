# Pyabtest
Simple tool to calculate P-value after conducting an A/B experiment

## A/B experiment & Hypothesis testing
Normally we run an A/B experiment to see whether a new model brings some improvement in the production metrics. After running the experiment for a fixed time period, we use hypothesis testing to scientifically come to a conclusion whether to accept the new feature or not. Usually, hypothesis testing has following components:

**Null hypothesis**: New model does not bring any improvement
**Alternative hypothesis**: New model does bring some improvement

This tool will be useful to calculate P-value to check whether we can reject the null hypothesis or not.

## Installation

Use the package manager `pip` to install pyabtest

``` python
pip install pyabtest
```

## Usage
Following functionalities are exposed in this package


## 1. Test for Sample Ratio Mismatch (SRM)
This is a test to check whether we have created audience for control vs test in a truly random manner. If there is an SRM, we should discard the A/B test results as control and variant have different type of audience. For example, we can pass following numbers in control vs test to check for SRM.

1. Number of male vs Number of female
2. Number of users of age < 40 vs Number of users of age >= 40
3. Number of active users vs Number of inactive users
4. Number of english speaking users vs Number of non-english speaking users
5. Number of mobile users vs Number of desktop users

**Input**: Control group 1 size, Control group 2 size, Variant group 1 size, Variant group 2 size
**Output**: P-value, Decision

``` python
>>> import pyabtest
>>> pyabtest.test_for_sample_ratio_mismatch(control_group1_size=1000,control_group2_size=2000,variant_group1_size=
1010,variant_group2_size=1990,alpha=0.05)
{'P-value': 0.78445, 'Alpha value (significance level)': 0.05, 'Decision': "Don't discard A/B test results"}
```

**Test used**: Chi-squared Test


## 2. Test for Binary Metric

This test can be used when when the result/action/feedback is binary & we want to see if variant observations are coming from a differant population when compared to control. For example, this test can be used in the following situations:

1. Clicks vs No clicks
2. Cart vs No cart
3. Order vs No order
4. Number of zero search results vs Number of non-zero serach results
5. Number of successful sessions vs Number of non-successful sessions
6. Number of positive reviews vs Number of negative reviews
7. Number of converted users vs Number of non-converted users

**Input**: No. of success in Control, No. of failures in Control, No. of success in variant, No. of failures in variant
**Output**: P-value, Decision

``` python
>>> import pyabtest
>>> pyabtest.test_for_binary_metric(control_success=50, control_failures=1000, variant_success=40, variant_failure
s=900, alpha=0.05)
{'P-value': 0.58718, 'Alpha value (significance level)': 0.05, 'Decision': 'Do not reject null hypothesis'}
```


**Test used**: Chi-squared Test

## 3. Test for Numeric Metric

This test can be used for any generic numeric metric (Count or Fraction). We can use this test even if the observations do not follow a normal distribution. In general, this test does not assume anything about the distribution as it is a non-parametric test. Example metrics include:

1. Number of clicks per unique user
2. Number of carts per unique user
3. Number of orders per unique user
4. Clicks/Views per unique user
5. Orders/Views per unique user
6. Orders/Session per unique user
7. Revenue per unique user
8. Session time per unique user
9. Order value per unique user
10. Successful sessions per unique user

**Input**: Control array, Variant array
**Output**: P-value, Decision


``` python
>>> import pyabtest
>>> from numpy import random
>>> pyabtest.test_for_numeric_metric(control_observations=random.randint(100, size=(20)), variant_observations=ran
dom.randint(100, size=(20)), alpha=0.05, no_of_samples=10000)
{'P-value': 0.7411, 'Alpha value (significance level)': 0.05, 'Decision': 'Do not reject null hypothesis'}
```

**Test used**: Bootstrap Test

## License
[MIT](https://choosealicense.com/licenses/mit/)


## References
1. **[Hypothesis testing](https://en.wikipedia.org/wiki/Statistical_hypothesis_testing)**
2. **[Chi-squared test](https://en.wikipedia.org/wiki/Chi-squared_test)**
3. **[Bootstrap test](https://en.wikipedia.org/wiki/Bootstrapping_(statistics))**


## Author
- [Rama Badrinath](https://www.linkedin.com/in/rama-badrinath-00405712). Email: ramab1988@gmail.com
