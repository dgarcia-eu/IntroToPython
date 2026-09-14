score = 72
if score >= 70:
    print("distinction")
elif score >= 50:
    print("pass")
else:
    print("fail")

# The order of the tests is the whole point. Put 'score >= 50' first and a score of
# 72 prints 'pass', because Python takes the FIRST branch that is true and skips
# the rest. Try swapping them to see it happen.
