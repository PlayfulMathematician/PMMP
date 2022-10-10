from PMMP import main
import matplotlib.pyplot as plt

a = main.NumFunc(lambda g: main.Polynomial(-1, 0, 10, 10).solve(guess=g, iterations=100))
plt.plot(list(range(-100, 100)), list(map(a, range(-100, 100))))
plt.show()
