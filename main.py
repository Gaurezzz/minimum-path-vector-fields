from src.minimum_path_algorithm import Minimum_Path_Algorithm
from src.vector_field_functions.gire import Gire
from src.vector_field_functions.shear import Shear
from src.vector_field_functions.turb import Turb
from src.vector_field_functions.windy import Windy
from src.vector_field_functions.channel_flow import Channel_flow
from src.vector_field_functions.cavity_flow import Cavity_flow
from src.track_simulation import Track_Simulation
from manim import *

class Shear_Simulation(Track_Simulation):

    vector_field = Shear(100, 100)
    velocity_factor = 2
    steady = False

class Windy_Simulation(Track_Simulation):

    vector_field = Windy(100, 100)
    velocity_factor = 2
    steady = False

class Gire_Simulation(Track_Simulation):

    vector_field = Gire(100, 100)
    velocity_factor = 2
    steady = False

class Channel_Flow_Simulation(Track_Simulation):

    vector_field = Channel_flow()
    velocity_factor = 2

class Cavity_Flow_Simulation(Track_Simulation):

    vector_field = Cavity_flow()
    initial_position_x = 1
    initial_position_y = 1
    final_position_x = 90
    final_position_y = 90
    velocity_factor = 2


