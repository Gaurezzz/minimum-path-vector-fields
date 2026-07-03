import numpy as np
from matplotlib import pyplot as plt
from src.vector_field_functions.vector_field import VectorField

class Turb(VectorField):

    def __init__(self, nx, ny):

        super().__init__(nx, ny, x_min = -np.pi, x_max = np.pi, y_min = -np.pi, y_max = np.pi, maximum_velocity=10)

        self.C = 0.1
        self.L = np.pi
        self.H = np.pi


    def get_point_by_position(self, x: float, y: float, t: float) -> tuple[float, float]:

        ξ = (x + self.L - self.C * t) % (2 * self.L) - self.L
        η = (y + self.H + 0 * t) % (2 * self.H) - self.H

        ψ = np.sin(ξ) + 0.7 * np.sin(η + 0.8 * np.sin(ξ)) + 0.3 * np.sin(2 * ξ - 3 * η)

        u = (ψ - np.roll(ψ, -1, axis=1)) / (self.L / (self.nx-1)) * 10 # dψ/dy
        v = - (ψ - np.roll(ψ, -1, axis=0)) / (self.H / (self.ny-1)) * 10 # -dψ/dx

        return float(u), float(v)
