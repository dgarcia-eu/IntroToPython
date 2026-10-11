# What is wrong with AI_grade_calculator.py
# =========================================
#
# Nineteen separate problems in 47 lines. They are grouped by how much damage
# they do, because that is the part worth arguing about: most people's list
# starts with the naming and the comments, and those are the least important
# things here.
#
# This whole file is comments. Running it does nothing, which is the point:
# nothing in AI_grade_calculator.py should be executed to study it.


# -----------------------------------------------------------------------
# DANGEROUS: these are the ones that matter
# -----------------------------------------------------------------------

# 1. eval() on whatever the user typed            line 11, fed from line 38
#    eval runs its argument as Python. A "grade" of __import__('os').remove('x')
#    deletes a file. This is not a style problem, it is a way in. To turn text
#    into a number, use int(g) or float(g), which can only ever give you a
#    number or an error.

# 2. Bare except that does nothing                lines 13-14
#    "except: pass" catches everything: the eval above blowing up, a typo in a
#    variable name, and Ctrl+C. The program cannot fail visibly, so every bug
#    below it is invisible too. Catch the error you expect, by name:
#    "except ValueError:", and say something.

# 3. Two star imports                             lines 2-3
#    "from os import *" brings in os.open and quietly replaces the built-in
#    open() with it. They are not the same function: os.open(path, flags)
#    returns a number, not a file. "from math import *" shadows pow() the same
#    way. Nothing warns you. Import the module: "import os", then "os.remove".


# -----------------------------------------------------------------------
# WRONG ANSWERS: it runs, and it lies to you
# -----------------------------------------------------------------------

# 4. Off-by-one, twice over                       lines 19-21
#    range(1, len(list)) starts at 1, so the first grade is never added. The
#    total is then divided by the full length anyway. For [90, 80] it reports
#    40. Both halves are wrong, and they do not cancel out.

# 5. Removing from a list while looping over it   lines 25-27
#    Removing an item shifts everything after it down one, while the loop
#    counter keeps going up, so the next item is skipped. [90, 40, 30] loses
#    the 40 and keeps the 30. Build a new list instead:
#    list = [g for g in list if g >= PASS_MARK]

# 6. Mutable default argument                     line 8
#    grades=[] is created once, when the function is defined, not once per
#    call. Every call shares the same list, so it fills up across calls and
#    across tests. Use grades=None, then "if grades is None: grades = []".

# 7. Comparing floats with ==                     line 30
#    avg == 100.0 is only ever True if the division lands exactly on 100.0.
#    Averages that should be 100 often are not, by a fraction too small to
#    print. Compare with a tolerance, or compare integers.

# 8. Crashes on no input                          line 21
#    Type "done" straight away and the list is empty, so the division is 0/0
#    and the program dies with ZeroDivisionError. Check for the empty case
#    before dividing.


# -----------------------------------------------------------------------
# WILL BITE SOMEONE LATER
# -----------------------------------------------------------------------

# 9.  Shadowing the built-in list                 line 5
#     After "list = []" the name list means that list, so list() stops working
#     anywhere below. Name it grades.

# 10. Globals mutated from several functions      lines 9, 17
#     add_grade and Average both reach out and change module-level state, so
#     you cannot tell what either does by reading it. Pass values in, return
#     values out.

# 11. main() runs on import                       line 47
#     Importing this file to reuse one function starts the input loop. Guard
#     it: "if __name__ == '__main__': main()".

# 12. Average() called twice                      lines 43-44
#     Once to print, once to test. It recomputes, and with all the global
#     state above, the two calls are not guaranteed to agree. Store the result.

# 13. Magic number 50                             line 26
#     The pass mark appears as a bare 50 with nothing saying what it is. Name
#     it: PASS_MARK = 50.

# 14. Hardcoded password, never used              line 6
#     A secret in source code is a secret in git history forever. This one is
#     not even used, which is worse: nobody will dare delete it.


# -----------------------------------------------------------------------
# STYLE: real, but fix these last
# -----------------------------------------------------------------------

# 15. Unreachable code after return               line 34
#     The print can never run. Usually the sign of an edit left half-finished.

# 16. if x: return True else: return False        lines 30-33
#     The comparison is already True or False. "return avg == 100.0".

# 17. Inconsistent naming                         throughout
#     Average is capitalised like a class, add_grade is not; g and x say
#     nothing about what they hold.

# 18. A comment that is not true                  line 1
#     "Works perfectly, DO NOT TOUCH!!!" is wrong on both counts. A confident
#     comment is not evidence. Comments are not checked by anything.

# 19. String concatenation instead of an f-string line 43
#     "Your average is: " + str(Average()) works, but
#     f"Your average is: {avg}" is shorter and does the str() for you.


# -----------------------------------------------------------------------
# The point
# -----------------------------------------------------------------------
#
# This code runs. It prints an average and does not complain. Everything in
# the first two groups is invisible unless you check whether the answer is
# plausible, which is the same lesson as the silent wrong answer in
# Day4/41_modules_exceptions.ipynb.
#
# A chatbot will hand you code like this, confidently. Reading it is the job.
