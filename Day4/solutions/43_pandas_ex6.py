# Quick question: what was the parameter inplace for?
# It decides whether the method changes the data frame you called it on, or hands
# you back a new one and leaves the original alone.
#
#   df.sort_values("age")                 returns a sorted COPY; df is untouched
#   df.sort_values("age", inplace=True)   sorts df itself and returns None
#
# That is why the cell above had to be run before df looked sorted, and why the
# cell after it showed df unsorted again: the second call had no inplace=True.

print("first three ages as stored:", list(df.age.head(3)))

sorted_copy = df.sort_values("age")          # a new frame
print("sorted copy :", list(sorted_copy.age.head(3)))
print("df unchanged:", list(df.age.head(3)))

# Prefer assigning the result. It reads better, it works in a chain, and pandas
# is moving away from inplace= altogether:
df = df.sort_values("age")
print("after assigning back:", list(df.age.head(3)))
