#!/usr/bin/env/python3
import pandas as pd
from matplotlib import pyplot as plt

input = pd.read_csv("res_benchmark.csv")

plt.plot(input["laenge"], input["dp_time"], label="Dynamic Programming")
plt.plot(input["laenge"], input["rec_time"], label="Recursive")

plt.xlabel("Sequence Length")
plt.ylabel("Time per Alignment")
plt.title("Comparison of Alignment Algorithms, Recursiv and Dynamic Programming")
plt.legend()
plt.savefig("benchmark.png")
plt.show()