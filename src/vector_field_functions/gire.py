import numpy as np
from matplotlib import pyplot as plt
from src.vector_field_functions.vector_field import VectorField

class Gire(VectorField):

    def __init__(self, nx, ny):

        super().__init__(nx, ny, x_min = -np.pi, x_max = np.pi, y_min = -np.pi, y_max = np.pi, maximum_velocity=10)

        self.C = 0.3
        self.L = np.pi
        self.H = np.pi


    def get_point_by_position(self, x: float, y: float, t: float) -> tuple[float, float]:

        ξ = (x + self.L - self.C * t) % (2 * self.L) - self.L
        η = (y + self.H + 0 * t) % (2 * self.H) - self.H

        u = np.sin(ξ) * np.cos(η) * 10
        v = -np.cos(ξ) * np.sin(η) * 10

        return float(u), float(v)
