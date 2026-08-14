# 2 - ALMOST
names = ['bernice', 'cody', 'aaron', 'ever', 'dalia']
long_names = [name.upper() for name in names if len(name) > 4]
print(long_names)

# 3 - ON YOUR OWN
prices = [4.5, 12.0, 30.0, 8.25, 99.9]
with_vat = [p * 1.19 for p in prices if p > 10]
print(with_vat)

# If a comprehension ever stops making sense, write the loop first and convert it
# afterwards. These two are the same thing:
with_vat = []
for p in prices:
    if p > 10:
        with_vat.append(p * 1.19)
print(with_vat)
