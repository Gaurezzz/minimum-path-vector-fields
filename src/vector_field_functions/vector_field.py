import numpy as np
from matplotlib import pyplot as plt
from abc import ABC, abstractmethod

class VectorField(ABC):
    """Abstract base class representing a 2D vector field over a discretized rectangular spatial grid.

    This class provides the foundation for defining static or dynamic mathematical flow fields.
    Subclasses must implement the abstract method `get_point_by_position` to define the analytical or
    numerical velocity components (u, v) at any continuous coordinate (x, y) and time t.

    Attributes:
        nx (int): Number of grid points along the x-axis.
        ny (int): Number of grid points along the y-axis.
        x_min (int | float): Minimum physical boundary coordinate of the domain along the x-axis.
        x_max (int | float): Maximum physical boundary coordinate of the domain along the x-axis.
        y_min (int | float): Minimum physical boundary coordinate of the domain along the y-axis.
        y_max (int | float): Maximum physical boundary coordinate of the domain along the y-axis.
        maximum_velocity (float): Maximum possible flow velocity magnitude across the domain,
            used for heuristic calculations and normalization.
        x (np.ndarray): 1D array of `nx` linearly spaced physical x-coordinates.
        y (np.ndarray): 1D array of `ny` linearly spaced physical y-coordinates.
        X (np.ndarray): 2D meshgrid array of x-coordinates (indexed with 'ij').
        Y (np.ndarray): 2D meshgrid array of y-coordinates (indexed with 'ij').
    """

    def __init__(self, nx: int, ny: int, x_min: int, x_max: int, y_min: int, y_max: int, maximum_velocity: float = np.inf):
        """Initializes the vector field domain, spatial grid arrays, and velocity limits.

        Args:
            nx (int): Number of discrete grid points along the x-axis.
            ny (int): Number of discrete grid points along the y-axis.
            x_min (int): Minimum coordinate boundary of the x-axis.
            x_max (int): Maximum coordinate boundary of the x-axis.
            y_min (int): Minimum coordinate boundary of the y-axis.
            y_max (int): Maximum coordinate boundary of the y-axis.
            maximum_velocity (float, optional): Maximum flow velocity magnitude in the field.
                Defaults to np.inf.
        """
        self.nx = nx
        self.ny = ny
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.maximum_velocity = maximum_velocity
        self.x = np.linspace(x_min, x_max, nx, endpoint=False)
        self.y = np.linspace(y_min, y_max, ny, endpoint=False)
        self.X, self.Y = np.meshgrid(self.x, self.y, indexing='ij')

    @abstractmethod
    def get_point_by_position(self, x: float, y: float, t: float) -> tuple[float, float]:
        """Calculates or retrieves the flow velocity components at a continuous physical coordinate and time.

        Args:
            x (float): Physical x-coordinate in the domain.
            y (float): Physical y-coordinate in the domain.
            t (float): Current simulation time.

        Returns:
            tuple[float, float]: A tuple (u, v) representing the horizontal and vertical velocity components.
        """
        pass

    def get_point_by_index(self, x: int, y: int, t: float) -> tuple[float, float]:
        """Retrieves the flow velocity components for a discrete grid index (x, y) at time t.

        Maps grid indices directly to physical coordinates on the internal `self.x` and `self.y` arrays.

        Args:
            x (int): Discrete grid index along the x-axis (0 <= x < nx).
            y (int): Discrete grid index along the y-axis (0 <= y < ny).
            t (float): Current simulation time.

        Returns:
            tuple[float, float]: A tuple (u, v) representing the horizontal and vertical velocity components.
        """
        return self.get_point_by_position(self.x[x], self.y[y], t)

    def get_limits(self) -> tuple[float, float, float, float]:
        """Returns the spatial boundaries of the vector field domain.

        Returns:
            tuple[float, float, float, float]: A tuple containing (x_min, x_max, y_min, y_max).
        """
        return (self.x_min, self.x_max, self.y_min, self.y_max)

    def get_maximum_velocity(self) -> float:
        """Retrieves the maximum expected flow velocity magnitude defined for this field.

        Returns:
            float: The maximum velocity magnitude across the domain.
        """
        return self.maximum_velocity
