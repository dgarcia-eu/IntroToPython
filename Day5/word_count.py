"""Count the words in a piece of text. Our first real script."""

text = "the old man and the sea"
words = text.split()

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print("words:", len(words))
print("counts:", counts)
