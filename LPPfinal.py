import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog


maxmin= input("Enter 'max' to maximize or 'min' to minimize: ")
c1 = float(input("Enter coefficient for x in objective function: "))
c2 = float(input("Enter coefficient for y in objective function: "))
n= int(input("Enter the number of constraints: "))

A, b = [], []
for i in range(n):
    print("Constraint "i)
    a1 = float(input("Enter coefficient of x: "))
    a2 = float(input("Enter coefficient of y: "))
    sign = input("Enter inequality type ('<=' or '>='): ").strip()
    c = float(input("Enter RHS value: "))

    if sign == ">=":
        A.append([-a1, -a2])
        b.append(-c)
    else:
        A.append([a1, a2])
        b.append(c)

if maxmin=="max":
    c = [-c1, -c2]
else :
    c=[c1, c2]

res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method="highs")

# Dynamically determine x and y range
x_min, x_max = 0, max([abs(c / a1) if a1 != 0 else 20 for (a1, a2), c in zip(A, b)] + [20])
y_min, y_max = 0, max([abs(c / a2) if a2 != 0 else 20 for (a1, a2), c in zip(A, b)] + [20])

x = np.linspace(x_min, x_max + 5, 400)


plt.figure(figsize=(10, 7))

for i, (a1, a2, c) in enumerate(zip(*np.array(A).T, b)):
    if a2 == 0: 
        plt.axvline(x=c/a1, linestyle='--', color='blue', label=f"Constraint {i+1}")
    else:
        y = (c - a1 * x) / a2
        plt.plot(x, y, label=f"Constraint {i+1}")


y_feasible = np.full_like(x, float('inf'))
for (a1, a2), c in zip(A, b):
    if a2 != 0:
        y_feasible = np.minimum(y_feasible, (c - a1 * x) / a2)

y_feasible = np.maximum(y_feasible, 0)  
plt.fill_between(x, 0, y_feasible, color="gray", alpha=0.3, label="Feasible Region")

if res.success:
    plt.scatter(res.x[0], res.x[1], color="red", label=f"Optimal (x={res.x[0]:.2f}, y={res.x[1]:.2f})")

plt.xlim(0, x_max + 2)
plt.ylim(0, y_max + 2)
plt.xlabel("x"), plt.ylabel("y"), plt.legend(), plt.title("LPP Graphical Solution")
plt.grid(), plt.show()

if res.success:
    if maxmin == "max":
        optimal_value = -res.fun
    else:
        optimal_value=res.fun
    print(f"\nOptimal Solution: x = {res.x[0]:.2f}, y = {res.x[1]:.2f}")
    print(f"Optimal Value of Z = {optimal_value:.2f}")
else:
    print("\nNo feasible solution found.")
