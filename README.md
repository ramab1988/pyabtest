# pyabtest
Simple tool to calculate P-value after conducting an A/B test

Normally we run an A/B test to see whether a new model brings some improvement in the production metrics.After running the experiment for a fixed time period, we use hypothesis testing to scientifically come to a conclusion whether to accept the new feature or not.

This tool will be handy to calculate P-value to check whether we can reject the null hypothesis or not.


pyabtest.test_for_sample_ratio_mismatch()
1. Number of male vs Number of female
2. Number of users < 40 vs Number of users > 40
3. Number of active users vs Number of inactive users

pyabtest.test_for_binary_metric()
Usecases:
1. Clicks vs No clicks
2. Cart vs No cart
3. Order vs No order
4. Test used: Chi-squared Pearson test

pyabtest.test_for_numeric_metric()
Usecases:
1. Number of clicks per unique user
2. Number of orders per unique user
3. Clicks/Views per unique user
4. Orders/Views per unique user
5. Orders/Session per unique user
6. Revenue per unique user
7. Session time per unique user
8. Order value per unique user

Test used: Bootstrap test
Note: We can use this test even if the observations do not follow a normal distribution. In general, this test does not assume anything about the distribution.
