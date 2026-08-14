# Final exam — what to expect

Handed out on Day 1 so there are no surprises on Friday. Nothing here is a secret: knowing the shape of the exam should let you spend your revision on Python rather than on guessing.

## The basics

| | |
|---|---|
| **When** | Friday morning, first thing — before the visualisation lecture |
| **How long** | 90 minutes |
| **Total** | 100 points |
| **To pass** | 50 points |
| **Conditions** | Closed book. No calculators, no computers, no notes. |

You also have to pass all five daily assignments (50% of 20 points each). The exam and the assignments are separate hurdles; doing well in one does not compensate for the other.

## What it is testing

**Whether you can read and reason about Python code.** Not whether you have memorised the notebooks.

You will not be asked to write a long program on paper. Where you do write code it will be a line or two. Most questions show you a short snippet and ask what it does — which means the skill to practise is *tracing code in your head*, line by line, keeping track of what each variable holds.

## The three kinds of question

Roughly speaking, the paper is:

- **About half — "what does this print?"** A short snippet; you write the output. If it raises an error, say which error and why. There are partial marks for identifying the error correctly even if your wording differs from ours.
- **About a third — "what goes wrong here, and why?"** Code that runs but does the wrong thing, or fails. You explain the cause in a sentence or two. These are the questions where understanding beats recall.
- **The rest — "write a line that does X."** One or two lines, not a program.

## What it covers

Everything from Monday to Thursday, plus Friday's material only insofar as it was covered before the exam. Expect questions drawn from across the whole week rather than concentrated in one day:

strings · lists · slicing · loops · if/elif/else · list and dictionary comprehensions · dictionaries · functions, return values and scope · `*args` and `**kwargs` · exceptions · reading and writing files, JSON · pandas

## How to prepare

1. **Do the daily quizzes properly.** Every morning starts with a few questions in the same style as the exam. They are ungraded and they are the closest thing to a mock paper you will get.
2. **Re-run the notebooks, and predict before you run.** Cover the output, say what you think will happen, then check. Where you are wrong, that gap is exactly what the exam is looking for.
3. **Do the Parsons problems and the faded examples.** They are in the notebooks, marked 🧩 and "Three at once". They train the tracing skill directly.
4. **Use the two-page reference** (`python_reference.md`). Not permitted in the exam, but it is the shortest revision list of everything the course actually used.
5. **Do not try to memorise the notebooks.** You will be asked about code you have never seen. Memorising examples is the least efficient way to prepare.

## Five example questions

Real questions, in the real format.

**1. (5 points)** Write the output of the following code.

```python
a = [1, 100]
b = a
b[0] = 0
print(a)
```

**2. (5 points)** Write the output. If it raises an error, briefly explain why.

```python
t = (1, 2, 3)
t.append(4)
```

**3. (5 points)** Look at the code below. State what it outputs, and explain in one or two sentences why.

```python
greeting = "hello"
greeting.upper()
print(greeting)
```

**4. (10 points)** Given `dictionary = {"applez": 100, "oranges": 120, "bananas": 50}`, write code that changes the key `"applez"` to `"apples"`, keeping its value.

**5. (15 points)** We want a function that adds five to its argument. Below is an attempt.

```python
def add_five(n):
    num_sum = 10
    new_n = n + 5
    return num_sum

print(add_five(20))
```

a) What does the last line print?
b) Explain why it does not print 25.
c) Rewrite `add_five(n)` so that it works.

<details>
<summary>Answers</summary>

1. `[0, 100]` — `b` is another name for the same list, not a copy, so changing `b` changes `a`.
2. `AttributeError` — tuples are immutable and have no `append` method.
3. `hello` — string methods return a new string and never modify the original, so the result was thrown away. It needed `greeting = greeting.upper()`.
4. `dictionary["apples"] = dictionary.pop("applez")`, or add the new key and `del` the old one. Keys cannot be renamed in place.
5. (a) `10`. (b) The function computes `new_n` but returns `num_sum`, so the computed value is discarded. (c) `def add_five(n): return n + 5`

</details>
