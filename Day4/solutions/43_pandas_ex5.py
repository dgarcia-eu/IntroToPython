# Quick exercises on groupby.

# 1. Fraction of rows with occupation "Tech-support", for each sex.
#    The trick: a column of True/False averages to the fraction that are True.
is_tech = df.occupation == "Tech-support"
print(is_tech.groupby(df.gender).mean())

# the same idea written out, if the line above is too compressed
df["is_tech"] = df.occupation == "Tech-support"
print(df.groupby("gender")["is_tech"].mean())

# 2. Mean hours per week for each combination of race and sex.
#    Group by a LIST of columns to get every combination.
print(df.groupby(["race", "gender"])["hours-per-week"].mean())
