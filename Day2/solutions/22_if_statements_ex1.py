print("####### Gymnast Scores")
scores = range(1,11)

for score in scores:
    if score == 1:
        print("A judge can give a gymnast {} point".format(score))
    if score > 1:
        print("A judge can give a gymnast {} points".format(score))

        
print("\n####### Numbers")
saved_numbers = [2, 1, 5, 12, 42, 34, 52]
new_numbers = [3, 1, 33, 52, 4]

for n in new_numbers:
    if n in saved_numbers:
        print("{} is already saved".format(n))
    if n not in saved_numbers:
        saved_numbers.append(n)
        print("{} is now saved".format(n))