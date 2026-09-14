# Exercise 3.5: average age per sex, as a bar chart.
# groupby gives one number per group, and a Series knows how to plot itself.
# Note the column here is called "sex" - the rename to "gender" happened in
# yesterday's pandas notebook, not in this one.
mean_age = df.groupby("sex")["age"].mean()
print(mean_age)

mean_age.plot(kind="bar")
plt.ylabel("mean age")
plt.xticks(rotation=0)
plt.show()
