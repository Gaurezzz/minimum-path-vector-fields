import numpy as np
from collections.abc import Callable
import heapq
from src.vector_field_functions.vector_field import VectorField
from src.vector_field_functions.gire import Gire


class Minimum_Path_Algorithm:
    """Implements an A* algorithm to find the minimum time path across a dynamic or steady vector field.

    This class calculates the optimal navigation route from an initial coordinate to a destination coordinate
    on a discretized grid. It accounts for both the constant inherent velocity of a navigating particle
    and the underlying flow velocities of the vector field at any given time.

    Attributes:
        vector_field (VectorField): The vector field instance providing flow velocity vectors and grid dimensions.
        nx (int): Number of grid points along the x-axis.
        ny (int): Number of grid points along the y-axis.
        maximum_velocity (float): Maximum magnitude of flow velocity in the vector field, used to compute an
            admissible heuristic for A* prioritization.
    """

    def __init__(self, vector_field: VectorField):

        self.vector_field = vector_field
        self.nx = vector_field.nx
        self.ny = vector_field.ny
        self.maximum_velocity = self.vector_field.get_maximum_velocity()

    def _invalid_coords(self, i: int, j: int):

        if i < 0 or i >= self.nx or j < 0 or j >= self.ny: return True
        else: return False

    def _calculate_time(self, c1i: int, c1j: int, c2i: int, c2j: int, particle_velocity: float, time: float):
        
        #calculate distance
        if c1i != c2i and c1j != c2j: distance=14.1421
        else: distance = 10

        θ=np.arctan2(c2j-c1j,c2i-c1i)

        v_vf_x, v_vf_y = self.vector_field.get_point_by_index(
            x = c1i,
            y = c1j,
            t = time
        )

        if np.abs(v_vf_x * np.sin(θ) - v_vf_y * np.cos(θ)) > particle_velocity: return np.inf, None, None, None

        v_r_1 = (v_vf_x * np.cos(θ) + v_vf_y * np.sin(θ)) + np.sqrt(particle_velocity**2 - (v_vf_x * np.sin(θ) - v_vf_y * np.cos(θ)) ** 2)
        v_r_2 = (v_vf_x * np.cos(θ) + v_vf_y * np.sin(θ)) - np.sqrt(particle_velocity**2 - (v_vf_x * np.sin(θ) - v_vf_y * np.cos(θ)) ** 2)

        if v_r_1 < 0 and v_r_2 < 0: return np.inf, None,None, None

        v_r = max(v_r_1, v_r_2)

        #calculate boat's angle
        vbx = v_r * np.cos(θ) - v_vf_x
        vby = v_r * np.sin(θ) - v_vf_y

        β = np.arctan2(vby, vbx)

        return (distance / v_r), β, v_vf_x, v_vf_y

    def A_star(self,
               initial_position_x: int,
               initial_position_y: int,
               final_position_x: int,
               final_position_y: int,
               particle_constant_velocity: float
               ) -> dict[str, list] | None:

        #Priority Queue: used to order coords regarding the distance
        pq = []

        # Finished Coords: used to identify coords already processed
        finished_coords = np.zeros((self.nx, self.ny), dtype=bool)

        #Track: used to save optimal path coordinates, and time
        track = {"x": [], "y": [], "t": [], "β": [], "u": [], "v": []}

        #Last Coord: used to save optimal last coord per coord
        last_coord = np.empty((self.nx, self.ny), dtype=object)

        #Last β: used to save boat vector's direction
        last_β = np.empty((self.nx, self.ny), dtype=object)

        #Last u and v: used to save vector field last direction
        last_u = np.empty((self.nx, self.ny), dtype=object)
        last_v = np.empty((self.nx, self.ny), dtype=object)

        #Best distance: used to save best distance found
        best_time = np.full((self.nx, self.ny), np.inf, dtype=float)
        best_time[initial_position_x, initial_position_y] = 0

        #Add first coord to priority queue
        initial_distance = 0
        heapq.heappush(pq, (initial_distance, initial_position_x, initial_position_y))

        while pq: #While we need to process more coords

            coord_distance, coord_x, coord_y = heapq.heappop(pq)

            #We should check if this coord hasn't been processed
            if finished_coords[coord_x, coord_y] == True: continue

            #mark it as processed
            finished_coords[coord_x, coord_y]=True

            #stop when finding the minimum reaching time 
            if coord_x == final_position_x and coord_y == final_position_y: break

            #We have to process the 8 coords around
            for i in range(coord_x-1, coord_x+2):
                for j in range(coord_y-1, coord_y+2):

                    #We shouldn't process the same coord
                    if i == coord_x and j == coord_y: continue 

                    #We should make sure the neightbord is inside the limits
                    if self._invalid_coords(i,j): continue

                    route_time, β, u, v = self._calculate_time(coord_x, coord_y, i, j, particle_constant_velocity, best_time[coord_x, coord_y])

                    #if we found a better route, we will update it 
                    if (best_time[coord_x, coord_y] + route_time < best_time[i,j]):

                        best_time[i,j]=best_time[coord_x, coord_y] + route_time
                        last_coord[i,j]=(coord_x, coord_y)
                        last_β[i,j]=β
                        last_u[i,j]=u
                        last_v[i,j]=v

                        #heuristic: minimum distance / particle's velocity
                        minimum_distance = np.sqrt((final_position_y - j) ** 2 + (final_position_x - i) ** 2) * 10
                        h = minimum_distance / (particle_constant_velocity + self.maximum_velocity)

                        heapq.heappush(pq, (best_time[i,j] + h, i, j))

        if best_time[final_position_x, final_position_y] == np.inf: return None

        pos_x = final_position_x
        pos_y = final_position_y

        while (pos_x, pos_y) != (initial_position_x, initial_position_y):
            track['x'].append(pos_x)
            track['y'].append(pos_y)
            track['t'].append(best_time[pos_x, pos_y])
            track['β'].append(last_β[pos_x, pos_y])
            track['u'].append(last_u[pos_x, pos_y])
            track['v'].append(last_v[pos_x, pos_y])
            pos_x, pos_y = last_coord[pos_x, pos_y]

        track['x'].reverse()
        track['y'].reverse()
        track['t'].reverse()
        track['β'].reverse()
        track['u'].reverse()
        track['v'].reverse()

        return track