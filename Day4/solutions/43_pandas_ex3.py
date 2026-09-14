# Quick exercise: describe what these do.
#   young = df[df.age < 40]      keeps only the rows where age is below 40.
#                                df.age < 40 is a column of True/False, one per
#                                row, and df[...] keeps the rows that are True.
#   len(young)                   counts how many rows survived the filter.

young = df[df.age < 40]
print("rows with age < 40:", len(young))
print("share of all rows:", len(young) / len(df))
