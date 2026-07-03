import numpy as np
from matplotlib import pyplot as plt
from src.vector_field_functions.vector_field import VectorField


class Cavity_flow(VectorField):

    def __init__(self):
        
        super().__init__(
            nx=100,
            ny=100,
            x_min=0,
            x_max=2,
            y_min=0,
            y_max=2,
            maximum_velocity=100
        )

        self.vf = np.load("data/cavity_flow.npy")

    def get_point_by_position(self, x: float, y: float, t: float) -> tuple[float, float]:
        
        Δx = (self.x_max - self.x_min)/(self.nx-1)
        Δy = (self.y_max - self.y_min)/(self.ny-1)

        ix = (x - self.x_min)/Δx
        iy = (y - self.y_min)/Δy

        i1 = int(max(min(np.floor(ix), self.nx-2),0))
        i2 = i1 + 1
        j1 = int(max(min(np.floor(iy), self.ny-2),0))
        j2 = j1 + 1

        fx = min(max(ix - i1, 0.0), 1.0)
        fy = min(max(iy - j1, 0.0), 1.0)

        prom_up_u = self.vf[i1, j2, 0]*(1-fx) + self.vf[i2, j2, 0]*fx
        prom_down_u = self.vf[i1, j1, 0]*(1-fx) + self.vf[i2, j1, 0]*fx
        prom_up_v = self.vf[i1, j2, 1]*(1-fx) + self.vf[i2, j2, 1]*fx
        prom_down_v = self.vf[i1, j1, 1]*(1-fx) + self.vf[i2, j1, 1]*fx

        prom_u = prom_down_u*(1-fy) + prom_up_u*fy
        prom_v = prom_down_v*(1-fy) + prom_up_v*fy

        return float(prom_u), float(prom_v)

    def get_point_by_index(self, x: int, y: int, t: float) -> tuple[float, float]:

        return self.vf[x,y,0], self.vf[x,y,1]


