# What is wrong with AI_grade_calculator.py
# =========================================
# Nineteen faults in 47 lines, grouped by how much damage they do. The grouping
# is the answer to the ranking half of the exercise. This file is comments only.

# --- DANGEROUS ---------------------------------------------------------------
# 1.  line 11, fed from 38  eval() runs whatever was typed as Python. Use int(g).
# 2.  lines 13-14           Bare except: pass hides every error, including Ctrl+C.
# 3.  lines 2-3             Star imports: "from os import *" replaces the built-in
#                           open() with os.open(path, flags). Nothing warns you.

# --- WRONG ANSWERS -----------------------------------------------------------
# 4.  lines 19-21           Skips the first grade AND divides by the full length,
#                           so [90, 80] reports 40. Two errors, not one.
# 5.  lines 25-27           Removing while looping skips items: [90, 40, 30] loses
#                           the 40 and keeps the 30.
# 6.  line 8                grades=[] is made once at definition, shared by all calls.
# 7.  line 30               avg == 100.0 compares floats exactly.
# 8.  line 21               Empty input divides by zero.

# --- WILL BITE LATER ---------------------------------------------------------
# 9.  line 5                list = [] shadows the built-in; list() stops working.
# 10. lines 9, 17           Globals mutated from two functions.
# 11. line 47               main() runs on import; needs if __name__ == "__main__".
# 12. lines 43-44           Average() computed twice, and need not agree.
# 13. line 26               The pass mark is a bare 50; name it PASS_MARK.
# 14. line 6                A hardcoded password, unused, in git history forever.

# --- STYLE -------------------------------------------------------------------
# 15. line 34               Unreachable print after return.
# 16. lines 30-33           if x: return True else: return False is return avg == 100.0.
# 17. throughout            Average is capitalised like a class; g and x say nothing.
# 18. line 1                "Works perfectly, DO NOT TOUCH!!!" is wrong on both counts.
# 19. line 43               Concatenation where an f-string is shorter.

# The first two groups are invisible from the output: the program runs and prints
# a confident wrong number. That is the whole lesson.
