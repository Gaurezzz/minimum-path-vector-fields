import numpy as np
from matplotlib import pyplot as plt
from src.vector_field_functions.vector_field import VectorField

class Windy(VectorField):

    def __init__(self, nx, ny):

        super().__init__(nx, ny, x_min = -np.pi, x_max = np.pi, y_min = -np.pi, y_max = np.pi, maximum_velocity=10)

        self.C = 0.1
        self.L = np.pi
        self.H = np.pi

        u_mesh = (np.cos(self.Y) * np.sin(self.X) + 0.3 * np.cos(2 * self.X + self.Y) - 0.4 * np.cos(self.X - 2 * self.Y)) * 10
        v_mesh = (-np.cos(self.X) * np.sin(self.Y) - 0.6 * np.cos(2 * self.X + self.Y) - 0.2 * np.cos(self.X - 2 * self.Y)) * 10
        
        self.maximum_velocity = float(np.max(np.hypot(u_mesh, v_mesh)))


    def get_point_by_position(self, x: float, y: float, t: float) -> tuple[float, float]:

        ξ = (x + self.L - self.C * t) % (2 * self.L) - self.L
        η = (y + self.H + 0 * t) % (2 * self.H) - self.H

        u = (np.cos(η) * np.sin(ξ) + 0.3 * np.cos(2 * ξ + η) - 0.4 * np.cos(ξ - 2 * η)) * 10
        v = (-np.cos(ξ) * np.sin(η) - 0.6 * np.cos(2 * ξ + η) - 0.2 * np.cos(ξ - 2 * η)) * 10

        return float(u), float(v)
