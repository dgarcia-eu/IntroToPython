# Python reference — everything this course uses

*"A summary sheet of all the important commands / python codes together would be cool for revision"* — student feedback, 2025. Here it is.

This is deliberately **only** what the course actually uses. If something is not here, you were not asked to know it. Organised by what you are trying to *do*, not by data type — because that is how you look things up when you are stuck.

Not permitted in the exam, but it is the shortest possible revision list.

---

## Working with text

```python
s = "The Old Man"
s.lower()             # 'the old man'          make it lowercase
s.upper()             # 'THE OLD MAN'
s.title()             # 'The Old Man'          capitalise each word
s.strip()             # remove spaces/newlines from both ends
s.replace("Old", "Young")
s.split()             # ['The', 'Old', 'Man']  split on whitespace
s.split(",")          # split on a specific character
" ".join(["a", "b"])  # 'a b'                  the opposite of split
len(s)                # 11                     how many characters
s.startswith("The")   # True
"Old" in s            # True                   substring test
```

**These return a new string. They never change the original.**
`s.upper()` on its own does nothing lasting — you need `s = s.upper()`.

```python
"{} is {}".format("python", "fun")   # 'python is fun'
print("a", "b")                      # a b        print adds spaces
"\n"   # newline        "\t"   # tab        "\\"   # a literal backslash
```

## Numbers

```python
7 + 2   # 9        7 / 2   # 3.5   always a float
7 - 2   # 5        7 // 2  # 3     floor division
7 * 2   # 14       7 % 2   # 1     remainder
7 ** 2  # 49                       to the power of

int("42")    float("3.1")    str(42)    round(3.7)
max([1, 5, 3])   min([1, 5, 3])   sum([1, 5, 3])   abs(-4)
```

## Lists

```python
xs = [3, 1, 2]
xs[0]        # 3        first item, counting from 0
xs[-1]       # 2        last item
len(xs)      # 3

xs.append(4)          # add ONE item to the end
xs.extend([5, 6])     # add EVERY item of another list
xs + [7]              # a new list, originals untouched
xs.insert(0, "first")
xs.remove(3)          # remove by VALUE   (ValueError if absent)
xs.pop()              # remove and return the last item
xs.index(2)           # position of a value
2 in xs               # True
xs.count(2)           # how many times 2 appears

sorted(xs)            # a NEW sorted list
xs.sort()             # sorts xs in place, returns None
xs.sort(reverse=True)
```

**`sorted()` gives you a new list. `.sort()` changes the one you have and returns `None`.**
`xs = xs.sort()` is a classic bug: it sets `xs` to `None`.

```python
list(range(5))        # [0, 1, 2, 3, 4]
list(range(1, 11))    # 1 to 10
list(range(0, 10, 2)) # [0, 2, 4, 6, 8]   with a step
```

## Slicing — works on lists *and* strings

```python
xs[1:4]     # from 1 up to but NOT including 4
xs[:3]      # first three
xs[3:]      # from 3 to the end
xs[-2:]     # last two
xs[::2]     # every second item
xs[::-1]    # reversed
```

## Tuples and sets

```python
t = (1, 2, 3)         # a tuple: like a list, but cannot be changed
t[0]                  # 1
# t.append(4)         -> AttributeError

s = {1, 2, 2, 3}      # a set: no duplicates, no order
set([1, 2, 2, 3])     # {1, 2, 3}   the usual way to remove duplicates
s.add(4)
```

## Loops

```python
for item in xs:
    print(item)

for i, item in enumerate(xs):        # position AND item
    print(i, item)

for a, b in zip(names, ages):        # two lists in step
    print(a, b)
```

The pattern behind most loops you will write — **build the answer up as you go**:

```python
total = 0                   # BEFORE the loop: start it off
for word in words:
    total = total + len(word)   # INSIDE: change it
print(total)                # AFTER: use it
```

`total = total + 1` can be shortened to `total += 1`.

## Conditions

```python
if score >= 70:
    print("distinction")
elif score >= 50:          # only tested if the first was False
    print("pass")
else:
    print("fail")
```

**Python takes the first branch that is true and skips the rest, so the order of your tests is the design.** Put the strictest condition first.

```python
==  equal        !=  not equal        <  <=  >  >=
and    or    not
x in xs        x not in xs
```

Falsy values — these all count as `False` in an `if`: `False`, `0`, `""`, `[]`, `{}`, `None`.

## Comprehensions

```python
[n * 2 for n in numbers]                    # transform every item
[n for n in numbers if n > 10]              # keep some items
[n * 2 for n in numbers if n > 10]          # both

{w: len(w) for w in words}                  # a dictionary comprehension
```

Read it as: **`[` what goes in the new list · `for` each item · `if` it passes `]`**

Every comprehension can be written as a loop, and a loop is never wrong:

```python
result = []
for n in numbers:
    if n > 10:
        result.append(n * 2)
```

## Dictionaries

```python
d = {"name": "ada", "age": 36}
d["name"]              # 'ada'      KeyError if the key is absent
d.get("email")         # None       no error
d.get("email", "-")    # '-'        with a fallback
d["email"] = "a@b.c"   # add or overwrite
del d["age"]
"name" in d            # True
len(d)

d.keys()      d.values()      d.items()

for key, value in d.items():
    print(key, value)
```

Counting things — the pattern behind Assignment 3:

```python
counts = {}
for word in words:
    if word not in counts:
        counts[word] = 1        # first time: create it
    else:
        counts[word] += 1       # after that: add to it
```

## Functions

```python
def greet(name, greeting="hello"):    # greeting has a default
    return greeting + " " + name

greet("ada")                  # 'hello ada'
greet("ada", "hi")            # positional
greet(name="ada")             # keyword

def anything(*args, **kwargs):
    # args   is a tuple of the extra positional arguments
    # kwargs is a dict  of the extra keyword arguments
    ...
```

**`return` hands the answer back. `print` only shows it.** A function that prints and does not return gives you `None`:

```python
def shout(t):
    print(t.upper())

x = shout("hi")     # prints HI
print(x)            # None - nothing was handed back
```

Variables made inside a function do not exist outside it.

```python
double = lambda x: x * 2                    # a small unnamed function
pairs.sort(key=lambda pair: pair[1])        # sort by the second element
```

## Errors

```python
try:
    total += value
except TypeError as e:      # catch one specific kind
    print("bad value:", e)
except Exception as e:      # catch anything else
    print(e)
else:
    print("no exception happened")
finally:
    print("this runs either way")
```

Read a traceback **from the bottom**: the last line names the error, and the arrow shows the line that caused it.

| error | usually means |
|---|---|
| `NameError` | typo, or you never ran the cell that defines it |
| `TypeError` | mixing incompatible types, e.g. `"a" + 1` |
| `IndexError` | list position that does not exist |
| `KeyError` | dictionary key that does not exist |
| `AttributeError` | method that this type does not have, e.g. `.append` on a tuple |
| `IndentationError` | spacing is inconsistent |
| `ValueError` | right type, impossible value, e.g. `int("hello")` |

## Files

```python
with open("file.txt") as f:        # 'r' read is the default
    text = f.read()                # the whole file as one string

with open("file.txt", "w") as f:   # 'w' OVERWRITES the file
    f.write("hello\n")

with open("file.txt", "a") as f:   # 'a' appends
    f.write("another line\n")
```

```python
import json
json.load(f)      # read from a FILE       json.dump(obj, f)   # write to a FILE
json.loads(s)     # read from a STRING     json.dumps(obj)     # write to a STRING
```

**The `s` is for string.** That is the whole rule.

## Modules

```python
import statistics
statistics.mean([1, 2, 3])

import statistics as st          # under a shorter name
from statistics import mean      # just one function
```

## Dates

```python
from datetime import datetime

d = datetime.strptime("Feb 09 2020", "%b %d %Y")   # PARSE:  string -> date
d.strftime("%Y-%m-%d")                             # FORMAT: date -> string
```

`%d` day · `%m` month number · `%b` month name · `%Y` four-digit year · `%H:%M:%S` time

**str-p-time parses. str-f-time formats.**

## pandas

```python
import pandas as pd

df = pd.read_csv("adult.csv", na_values="?")
df.head()          df.info()          df.describe()
df.columns         len(df)

df["age"]                       # one column
df[["age", "sex"]]              # several columns - note the double brackets
df.age                          # same as df["age"], only for simple names

df[df.age < 40]                             # rows matching a condition
df[(df.age >= 20) & (df.age <= 40)]         # & for and, | for or
df[df.education.isin(["Bachelors"])]        # matches any of a list
```

**Every condition needs its own parentheses, and it is `&` / `|`, not `and` / `or`.**

```python
df.education.unique()           df.education.value_counts()
df.age.mean()   .median()   .max()   .std()

df.sort_values("age")
df.sort_values(["age", "hours-per-week"], ascending=False)

df = df.rename(columns={"sex": "gender"})   # assign the result back!
df.groupby("education")["age"].mean()       # one number per group
df.to_csv("out.csv", index=False)
```

## Plotting

```python
import matplotlib.pyplot as plt

plt.plot(x, y, color="red", label="series 1")   # line
plt.scatter(x, y)                               # points
plt.bar(x, heights)                             # bars
plt.hist(values, bins=20)                       # histogram

plt.xlabel("day")      plt.ylabel("temperature")     plt.title("...")
plt.ylim(-5, 35)       plt.legend()                  plt.show()
plt.savefig("figure.png")
```

`plt.legend()` shows nothing unless each series was given a `label=`.

```python
df["age"].plot(kind="bar")      # plot straight from pandas
```

---

*Anything not on this page was not required by this course.*
