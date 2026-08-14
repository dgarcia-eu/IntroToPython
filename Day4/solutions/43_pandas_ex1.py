# Quick question: what happens with df.capital-gain?
# Python reads it as  df.capital - gain , i.e. "the attribute capital, minus the
# variable gain". There is no column called "capital" and no variable called
# "gain", so it fails. Attribute access only works for column names that are
# valid Python identifiers, so a name with a hyphen must use brackets.

df["capital-gain"].head()
