import numpy as np
import heapq

class Minimum_Path_Algorithm:

    def __init__(self, vector_field, resolution_x: int = 100, resolution_y: int = 100):

        #Upload vector field
        self.vf = vector_field
        self.nx = resolution_x
        self.ny = resolution_y

    def _invalid_coords(self, i: int, j: int):

        if i < 0 or i >= self.nx or j < 0 or j >= self.ny: return True
        else: return False

    def _calculate_time(self, c1i: int, c1j: int, c2i: int, c2j: int, particle_velocity: float):
        
        #calculate distance
        if c1i != c2i and c1j != c2j: distance=14.1421
        else: distance = 10

        θ=np.arctan2(c2j-c1j,c2i-c1i)

        v_vf_x = self.vf[c1i, c1j, 0]
        v_vf_y = self.vf[c1i, c1j, 1]

        if np.abs(v_vf_x * np.sin(θ) - v_vf_y * np.cos(θ)) > particle_velocity: return np.inf

        v_r_1 = (v_vf_x * np.cos(θ) + v_vf_y * np.sin(θ)) + np.sqrt(particle_velocity**2 - (v_vf_x * np.sin(θ) - v_vf_y * np.cos(θ)) ** 2)
        v_r_2 = (v_vf_x * np.cos(θ) + v_vf_y * np.sin(θ)) - np.sqrt(particle_velocity**2 - (v_vf_x * np.sin(θ) - v_vf_y * np.cos(θ)) ** 2)

        if v_r_1 < 0 and v_r_2 < 0: return np.inf

        return distance / max(v_r_1, v_r_2)

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
        track = {"x": [], "y": [], "t": []}

        #Last Coord: used to save optimal last coord per coord
        last_coord = np.empty((self.nx, self.ny), dtype=object)

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

                    route_time = self._calculate_time(coord_x, coord_y, i, j, particle_constant_velocity)

                    #if we found a better route, we will update it 
                    if (best_time[coord_x, coord_y] + route_time < best_time[i,j]):

                        best_time[i,j]=best_time[coord_x, coord_y] + route_time
                        last_coord[i,j]=(coord_x, coord_y)

                        #heuristic: minimum distance / particle's velocity
                        minimum_distance = np.sqrt((final_position_y - j) ** 2 + (final_position_x - i) ** 2) * 10
                        h = minimum_distance / particle_constant_velocity

                        heapq.heappush(pq, (best_time[i,j] + h, i, j))

        if best_time[final_position_x, final_position_y] == np.inf: return None

        pos_x = final_position_x
        pos_y = final_position_y

        while (pos_x, pos_y) != (initial_position_x, initial_position_y):
            track['x'].append(pos_x)
            track['y'].append(pos_y)
            track['t'].append(best_time[pos_x, pos_y])
            pos_x, pos_y = last_coord[pos_x, pos_y]

        track['x'].append(0)
        track['y'].append(0)
        track['t'].append(0)

        track['x'].reverse()
        track['y'].reverse()
        track['t'].reverse()

        return track

#TEST

vf = np.load('data/cavity_flow.npy')

MPA = Minimum_Path_Algorithm(vf)

print(MPA.A_star(1,1,98,98,10))

        


                    





