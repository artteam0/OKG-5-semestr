import numpy as np
import matplotlib.pyplot as plt
import math

def Lagr(X, Y, x):
    z = 0.0
    n = len(X)
    
    for i in range(n):
        p = 1.0
        for j in range(n):
            if i != j:
                p = p * (x - X[j]) / (X[i] - X[j])
        z = z + Y[i] * p
    return z

def Bezier(X, Y, M):
    n = len(X) - 1
    
    XB = []
    YB = []
    
    ts = np.linspace(0, 1, M + 1)
    
    for t in ts:
        xt = 0.0
        yt = 0.0
        for i in range(n + 1):
            binom = math.comb(n, i)
            bernstein = binom * ((1 - t)**(n - i)) * (t**i)
            
            xt += X[i] * bernstein
            yt += Y[i] * bernstein
        XB.append(xt)
        YB.append(yt)
        
    return np.array(XB), np.array(YB)


def func(x):
    return (2 + np.cos(x)) ** np.sin(2 * x)
x_nodes = np.arange(0, np.pi + 0.001, np.pi / 4)
y_nodes = func(x_nodes)

x_interp = np.arange(0, np.pi + 0.001, 0.2)
y_interp_lagr = [Lagr(x_nodes, y_nodes, x) for x in x_interp]

data_nodes = np.column_stack((x_nodes, y_nodes))
np.savetxt("nodes.txt", data_nodes, fmt='%.4f')

data_lagr = np.column_stack((x_interp, y_interp_lagr))
np.savetxt("lagrange.txt", data_lagr, fmt='%.4f')

print("Файлы 'nodes.txt' и 'lagrange.txt' успешно созданы.")

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Полином Лагранжа")
plt.scatter(x_nodes, y_nodes, color='red', label='Узлы (Nodes)', zorder=5)
plt.plot(x_interp, y_interp_lagr, color='blue', label='L(x) Интерполяция')
plt.grid(True)
plt.legend()
plt.xlabel("x")
plt.ylabel("y")

M = 50
xb, yb = Bezier(x_nodes, y_nodes, M)

plt.subplot(1, 2, 2)
plt.title("Кривая Безье")
plt.plot(x_nodes, y_nodes, 'ro--', label='Опорные точки (Control Points)')
plt.plot(xb, yb, 'g-', linewidth=2, label='Кривая Безье')
plt.grid(True)
plt.legend()
M = 50
xb, yb = Bezier(x_nodes, y_nodes, M)

data_bezier = np.column_stack((xb, yb))
np.savetxt("bezier.txt", data_bezier, fmt='%.4f')
print("Файл 'bezier.txt' создан.")

plt.tight_layout()
plt.show()