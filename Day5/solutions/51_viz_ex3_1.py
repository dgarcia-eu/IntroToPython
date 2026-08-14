# Exercise 3.1: two lines, with labels, a legend and a sensible y-axis.
plt.plot(weather_station_1, color="red", label="station 1")
plt.plot(weather_station_2, color="blue", label="station 2")
plt.xlabel("day")
plt.ylabel("temperature")
plt.ylim(-5, 35)
plt.legend()
plt.show()
