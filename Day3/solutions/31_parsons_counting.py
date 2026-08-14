words = ['sea', 'man', 'sea', 'old', 'sea']
counts = {}
for word in words:
    if word not in counts:
        counts[word] = 1
    else:
        counts[word] = counts[word] + 1
print(counts)

# This is the pattern Assignment 3 asks for. Note the two branches: the first time
# you meet a word you have to CREATE its entry, every time after you ADD to it.
# Forget the first branch and you get a KeyError on the very first word.
