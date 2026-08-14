print("Multiples of Ten")

print("Make a list of the first ten multiples of ten (10, 20, 30... 90, 100).")

first_tens = list(range(10,101,10))  # with range step by step
print(first_tens)

first_tens = []      # with a loop
for i in range(1,11):
	first_tens.append(i*10)
print(first_tens)


first_tens = [number * 10 for number in range(1,11)]  # with list comprehension
print(first_tens)

print("Cubes")

print("Make a list of the first ten cubes (1, 8, 27... 1000) using a list comprehension and print them out.")

first_cubes = [number**3 for number in range(1,11)]
print(first_cubes)


print("Working Backwards")
print("Write out the following code without using a list comprehension:")
plus_thirteen = [number + 13 for number in range(1,11)]

plus_thirteen = []
for number in range(1,11):
	plus_thirteen.append(number+13)
