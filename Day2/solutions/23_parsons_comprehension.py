words = ['the', 'old', 'man', 'and', 'the', 'sea', 'again']
long_words = [w.upper() for w in words if len(w) > 3]
print(long_words)

# Read the comprehension right to left the first few times:
#   for w in words        <- go through the words
#   if len(w) > 3         <- keep only the long ones
#   w.upper()             <- and this is what goes in the new list
# The same thing as a loop, which is always allowed:
long_words = []
for w in words:
    if len(w) > 3:
        long_words.append(w.upper())
print(long_words)
