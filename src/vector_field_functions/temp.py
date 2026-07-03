#%% Periodic Vector Fields

import numpy as np
from matplotlib import pyplot as plt


flow_field = "turb"

C = 1.0


# grid

L = np.pi

H = np.pi

x = np.linspace(-L, L, 100, endpoint=False)

y = np.linspace(-H, H, 100, endpoint=False)

X, Y = np.meshgrid(x, y)


def vector_field(X, Y, t):

# Periodic Coordinates transformation

ξ = (X + L - C * t) % (2 * L) - L

η = (Y + H + 0 * t) % (2 * H) - H

match flow_field:

case "gire": # double-gyre flow

u = np.sin(ξ) * np.cos(η)

v = -np.cos(ξ) * np.sin(η)

case "windy": # windy field (2d periodic)

u = np.cos(η) * np.sin(ξ) + 0.3 * np.cos(2 * ξ + η) - 0.4 * np.cos(ξ - 2 * η)

v = -np.cos(ξ) * np.sin(η) - 0.6 * np.cos(2 * ξ + η) - 0.2 * np.cos(ξ - 2 * η)

case "shear": # Shear flow (perodic in x-axis)

u = np.tanh(η) + 0.1 * np.sin(2 * ξ)

v = 0.1 * np.cos(2 * ξ)

case "turb": # Turbulent flow (2d periodic)

ψ = np.sin(ξ) + 0.7 * np.sin(η + 0.8 * np.sin(ξ)) + 0.3 * np.sin(2 * ξ - 3 * η)

u = (ψ - np.roll(ψ, -1, axis=1)) / (L / 101) # dψ/dy

v = - (ψ - np.roll(ψ, -1, axis=0)) / (H / 101) # -dψ/dx


return u, v




fig, ax = plt.subplots()

u, v = vector_field(X, Y, 0.0)

u_mag = np.sqrt(u**2 + v**2)

quiver = ax.quiver(X, Y, u, v, u_mag, pivot="middle", scale=15 )

ax.set_aspect("equal")

ax.set_xlabel("x")

ax.set_ylabel("y")


# Animate the vector field

for t in np.linspace(0, 2*np.pi, 100):

u, v = vector_field(X, Y, t)

quiver.set_UVC(u, v)

plt.draw()
plt.pause(0.1)