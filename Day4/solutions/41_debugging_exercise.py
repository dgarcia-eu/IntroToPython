# Two bugs.
#
# 1. KeyError on the first word. counts[word] is read before it exists, so there
#    has to be a branch that creates the entry the first time.
# 2. Even once that is fixed, the counts would be wrong if you "fixed" it by
#    writing counts[word] = 1 unconditionally - every word would end up at 1.
#    The create and the increment are two different cases.

def count_words(words):
    counts = {}
    for word in words:
        if word not in counts:
            counts[word] = 1          # first time we see it: create the entry
        else:
            counts[word] = counts[word] + 1   # after that: add to it
    return counts

print(count_words(['sea', 'man', 'sea']))     # {'sea': 2, 'man': 1}

# A shorter way, once you trust it:
def count_words_short(words):
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts

print(count_words_short(['sea', 'man', 'sea']))

# Check the answer is plausible before believing it: three words in, and the
# counts should add up to three.
