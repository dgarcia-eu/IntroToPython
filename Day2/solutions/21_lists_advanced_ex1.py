"""
Working List

    Make a list that includes four careers, such as 'programmer' and 'truck driver'.
"""
print("Part 1")
careers = ['doctor', 'scientist', 'historian', 'teacher']

print("\nUse the list.index() function to find the index of one career in your list.")
    
print(careers.index('historian'))

print("\nUse the append() function to add a new career to your list.")

careers.append('politician')
print(careers)

print("\nUse the insert() function to add a new career at the beginning of the list.")

careers.insert(0, 'archeologist')
print(careers)
print("\n")

"""
Ordered Working List
"""

print("Start with the list you created in Working List.")

print("\nUse a loop to print out the list in reversed alphabetical order using the function *sorted()*")

for career in sorted(careers, reverse = True):
    print(career)


print("\n")
"""
List Lengths
"""

print("\nPrint out a statement that tell us how long your list is.")

print("the new_careers list is {} items long.".format(len(careers)))
