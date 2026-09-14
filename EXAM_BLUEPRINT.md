# Introduction to Programming with Python - Final exam mode

The purpose of this document is to familiarize you with the mode of the final written exam of the course.
Knowing the shape of the exam should let you spend most of your time learning Python rather than doing guesswork about how the exam will be.
Questions about the exam are welcome during the course but I expect you to read this document the latest on **Day 1**.

## The basics

- **When:** Day 5 (Friday) in the morning, starting at **9:30**. The visualization session follows and is applied in the last assignment.
- **How long:** 90 minutes
- **Points:** a total of 100 points, with 50 needed to pass
- **Setup:** Closed book, no calculators, computers, mobile phones, nor notes.

Remember that you also have to pass all five daily assignments (50% of each) to pass the course.
The exam and the assignments are separate evaluations. Doing well in one does not compensate for the other, you have to pass all.

## What the written exam tests

**Whether you can read and reason about Python code.** Not whether you have memorized the notebooks or precise Python syntax or commands.
You will not be asked to write a long program on paper. You will have to write some code but it will be a line or two and what is evaluated is your
logic and understanding of the language and of programming concepts, not syntax or typos.
Most questions show you a short snippet and ask what it does.
The best skill to practice to prepare for that is *tracing code* in your head or on a sheet of paper, line by line, 
keeping track of what each variable holds.

## The three kinds of questions

- **"What does this print?"**  You get a short snippet, your task is to write its output. 
If it raises an error, say which error and why.
The particular punctuation and structure of the output does not matter as long as it is not a key component of your understanding. You should focus on showing that you know what happens rather than on getting each character right.
- **"What is wrong here, and why?"** 
You get code that runs but does the wrong thing or fails. Your task is to explain the cause for this failure in a sentence or two.
- **"Write a line that does X."** 
Might be in isolation or within the context of a larger program. This task asks for one or two lines, not a whole program. There can be many possible ways to solve this task.

## What it covers

Everything from Day 1 to Day 4. Expect questions drawn from across the whole week rather than concentrated in one day. A few things for you to check that you understand:

- strings 
- lists
- slicing
- loops
- conditionals
- list and dictionary comprehensions
- dictionaries
- functions, return values and scope
- exceptions
- reading and writing files, JSON
- pandas

## How to prepare

1. **Do the daily quizzes properly.** Every morning starts with a few questions in the same style as the exam for us to practice together.
They are ungraded but trying them live during the session is a great way to practice.
2. **Re-run the notebooks cell by cell and predict what happens before you run each cell.** 
Cover the output, say out loud what you think will happen, then check.
The parts where you are wrong are the gaps the exam is aiming to test.
If you don't understand something, you should ask the tutors.
You can also do this with a study partner and take turns and help each other to understand when the other doesn't.
Explaining code to other people will also help you to find gaps in your understanding.
3. **Do the Parsons problems and the faded examples.**
They are in the notebooks marked 🧩 and "Three at once". They train the skill of tracing code and understanding what it does.
4. **Use the two-page reference** (`python_reference.md`). 
Not permitted in the exam but it is a good summary of what we used during the course.
You can also call it the cheat sheet, have it close to you when you are practicing.
5. **Do not try to memorize the notebooks.** 
You will be asked about code you have never seen. Memorizing examples or slides does not prepare you for the exam.
If there is any similar code, it will be slighlty different and memorizing will lead to mistakes.

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
