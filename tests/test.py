from PMMP import main
a = main.NumFunc(lambda g: main.Polynomial(-1, 0, 10, 10).solve(guess=g, iterations=100))
import matplotlib.pyplot as plt
plt.plot(list(range(-100, 100)), list(map(a, range(-100, 100))))
plt.show()