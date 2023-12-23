from itertools import count
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy import cos, sin
from scipy.integrate import odeint

g = 9.8

l1 = 1
l2 = 1

m1 = 1
m2 = 1

y0 = [np.pi / 2, 0, np.pi, 0]


def pendulo_duplo(x, t):
    x1, x2, x3, x4 = x

    dxdt = [
        x2,
        (
            -g * (2 * m1 + m2) * sin(x1)
            - m2 * g * sin(x1 - 2 * x3)
            - 2 * sin(x1 - x3) * m2 * (x4**2 * l2 + x2**2 * l1 * cos(x1 - x3))
        )
        / (l1 * (2 * m1 + m2 - m2 * cos(2 * x1 - 2 * x3))),
        x4,
        (
            2
            * sin(x1 - x3)
            * (
                x2**2 * l1 * (m1 + m2)
                + g * (m1 + m2) * cos(x1)
                + x4**2 * l2 * m2 * cos(x1 - x3)
            )
        )
        / (l2 * (2 * m1 + m2 - m2 * cos(2 * x1 - 2 * x3))),
    ]

    return dxdt


t = np.linspace(start=0, stop=50, num=2000)

results = odeint(func=pendulo_duplo, y0=y0, t=t)

theta1 = results[:, 0]
theta2 = results[:, 2]

X1 = l1 * sin(theta1)
Y1 = -l1 * cos(theta1)

X2 = l1 * np.sin(theta1) + l2 * np.sin(theta2)
Y2 = -l1 * np.cos(theta1) - l2 * np.cos(theta2)

x2 = []
y2 = []

fig, axs = plt.subplots()
fig.suptitle("Double Pendulum")
axs.plot(x2, y2)

counter = count(0, 1)


def update(_):
    idx = next(counter)
    if idx < len(X2):
        # plot barra 1
        l1x = [0, X1[idx]]
        l1y = [0, Y1[idx]]

        # plot barra 2
        l2x = [X1[idx], X2[idx]]
        l2y = [Y1[idx], Y2[idx]]

        # plot trilha
        x2.append(X2[idx])
        y2.append(Y2[idx])

        plt.cla()

        axs.plot(l1x, l1y, color="b", linewidth=2)
        axs.plot(l2x, l2y, color="b", linewidth=2)
        axs.plot(x2, y2, color="r", linewidth=1)

        axs.set_xlim(left=-l1 - l2 - 0.5, right=l1 + l2 + 0.5)
        axs.set_ylim(top=l1 + l2 + 0.5, bottom=-l1 - l2 - 0.5)


ani = FuncAnimation(fig=fig, func=update, interval=1, frames=300)
plt.show()
