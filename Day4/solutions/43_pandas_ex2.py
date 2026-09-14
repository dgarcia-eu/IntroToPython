# Quick question: why "df = df.rename(...)"? Is there another way?
# Because rename() does not change the data frame in place: it returns a NEW one
# and leaves the original untouched. If you do not assign the result, the change
# is thrown away. The alternative is inplace=True, which modifies df directly.

df = df.rename(columns={"sex": "gender"})     # returns a new frame, so assign it
df.rename(columns={"sex": "gender"}, inplace=True)   # or modify in place

# Prefer the first form. It is easier to read, it works in a chain of operations,
# and pandas is moving away from inplace=True.
