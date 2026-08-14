# 2 - ALMOST
def average(numbers):
    total = sum(numbers)
    return total / len(numbers)

print(average([2, 4, 6]))

# 3 - ON YOUR OWN
def initials(first, last):
    return first[0].upper() + "." + last[0].upper() + "."

print(initials('ada', 'lovelace'))

# Watch what changes if you use print() instead of return:
def average_printed(numbers):
    print(sum(numbers) / len(numbers))

x = average_printed([2, 4, 6])   # prints 4.0 ...
print(x)                         # ... but x is None: nothing was handed back
