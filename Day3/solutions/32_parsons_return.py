def initials(first, last):
    return first[0].upper() + "." + last[0].upper() + "."

print(initials("ada", "lovelace"))

# Two things to notice. The body has to be indented under the def, and the call has
# to come AFTER the definition - Python reads top to bottom, so calling it first is
# a NameError. And because the function RETURNS rather than prints, the caller
# decides what to do with the answer.
