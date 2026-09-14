words = ['the', 'old', 'man', 'and', 'the', 'sea']
total = 0
for word in words:
    total = total + len(word)
print(total)

# The order that matters: 'total' must exist BEFORE the loop, the line that adds
# to it must be INSIDE the loop, and the print must come AFTER the loop.
# Move print(total) inside the loop and you get a running total instead - which is
# a useful thing to want, and exactly what Assignment 1 asks for.
