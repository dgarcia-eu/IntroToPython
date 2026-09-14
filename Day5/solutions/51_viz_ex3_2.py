# Exercise 3.2: a paired bar chart.
# The idea: draw each series at the same tick positions, but nudge one set left
# and the other right by half a bar width, so the pairs sit side by side.
x = np.arange(len(parties))
width = 0.4

plt.figure(figsize=(9, 4))
plt.bar(x - width/2, result_2013, width=width, label="2013")
plt.bar(x + width/2, result_2017, width=width, label="2017")

plt.xticks(x, parties, rotation=45, ha="right")
plt.ylabel("share of the vote (%)")
plt.legend()
plt.tight_layout()
plt.show()
