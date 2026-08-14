names = ['bernice', 'cody', 'aaron', 'ever', 'dalia']
last_three = names[-3:]
last_three = last_three[::-1]
print(last_three)

# You can also do both slices in one step, because slicing a slice is still a slice:
print(names[-3:][::-1])
