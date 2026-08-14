# 2 - ALMOST
words = ['the', 'old', 'man', 'and', 'the', 'sea', 'again']
long_count = 0
for word in words:
    if len(word) > 3:
        long_count = long_count + 1     # or: long_count += 1
print(long_count)

# 3 - ON YOUR OWN
words = ['the', 'old', 'man', 'and', 'the', 'sea']
first_letters = []                      # before: an empty list to fill
for word in words:
    first_letters.append(word[0])       # inside: add to it
print(first_letters)                    # after: use it

# The accumulator does not have to be a number. A list works the same way:
# start empty, append inside the loop, use it afterwards.
