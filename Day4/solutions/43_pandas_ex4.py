# Quick questions about .agg([lowend, highend])
# 1. We apply two functions to the same column in one go, and get one result per
#    function: the 5% and the 95% quantile of age.
# 2. To add the median in the middle, define it and list it in that order -
#    .agg() keeps the order you give.
# 3. Yes, there is more than one way: a named lambda, or the string "median",
#    or df.age.quantile([0.05, 0.5, 0.95]).

def lowend(x):
    return x.quantile(0.05)

def middle(x):
    return x.quantile(0.50)

def highend(x):
    return x.quantile(0.95)

print(df.age.agg([lowend, middle, highend]))

# the same thing with a built-in name, and again in a single call
print(df.age.agg([lowend, "median", highend]))
print(df.age.quantile([0.05, 0.50, 0.95]))
