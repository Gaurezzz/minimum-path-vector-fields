from manim import *
import numpy as np
from scipy.interpolate import RegularGridInterpolator, interp1d
from minimum_path_algorithm import Minimum_Path_Algorithm

class Track_Simulation(ZoomedScene):

    nx: int = 100
    ny: int = 100
    map_height: float = 7.6
    map_width: float = 7.6
    vector_field_values = ""
    velocity_factor = 1

    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoomed_display_width=5.4,
            zoomed_display_height=5.4,
            
            zoom_factor=0.25, 
            
            **kwargs
        )

    def create_vector_field(self):

        X = np.arange(self.nx)
        Y = np.arange(self.ny)

        self.interp_vx = RegularGridInterpolator(
            points = (X, Y), 
            values = self.vector_field_values[:, :, 0],
            bounds_error=False,
            fill_value=0
            )
        self.interp_vy = RegularGridInterpolator(
            points = (X, Y), 
            values = self.vector_field_values[:, :, 1],
            bounds_error=False,
            fill_value=0
            )

        def function(v: np.ndarray) -> np.ndarray:
            vx = self.interp_vx([[v[0], v[1]]])[0]
            vy = self.interp_vy([[v[0], v[1]]])[0]
            return np.array([vx, vy, 0])

        self.vf_streamLines = StreamLines(
            func=function,
            x_range=[0, self.nx, 2],
            y_range=[0, self.ny, 2],
            color=BLUE
        )

        self.vf_streamLines.move_to(np.array([self.map_width/2 - 0.75, 0, 0]))
        self.vf_streamLines.set(height=self.map_height, width=self.map_width)
        self.vf_streamLines.set_stroke(width=3.5)

        self.add(self.vf_streamLines)
        self.vf_streamLines.start_animation(warm_up=False, flow_speed=0.5*self.velocity_factor)

    def find_track(self):

        MPA = Minimum_Path_Algorithm(self.vector_field_values)

        track = MPA.A_star(
            initial_position_x=1,
            initial_position_y=1,
            final_position_x=98,
            final_position_y=98,
            particle_constant_velocity=10
            )

        if track is None: 
            self.tx = None
            self.ty = None
            return

        track['x'] = np.array(track['x']) / 100 * self.map_width - 0.75
        track['y'] = np.array(track['y']) / 100 * self.map_height - 3.8
        track['t'] = np.round(np.array(track['t']), 2)

        #Set time as a soft function
        self.tx = interp1d(track['t'], track['x'], kind='cubic', bounds_error=False, fill_value="extrapolate")
        self.ty = interp1d(track['t'], track['y'], kind='cubic', bounds_error=False, fill_value="extrapolate")
        self.total_time = track['t'][-1]

    def create_no_path_animation(self):

        self.create_vector_field()
        text = Text(text = "There is not a valid track \nfor this vector field :(")
        text.next_to(self.vf_streamLines, LEFT, buff=0.5)
        text.scale_to_fit_width(5.5)
        self.play(Write(text))
        self.wait(10)

    def move_boat(self, boat, dt):
        current_time = self.time_tracker.get_value()
        new_x = self.tx(current_time)
        new_y = self.ty(current_time)
        boat.move_to(np.array([new_x, new_y, 0]))


    def create_path_animation(self):

        self.create_vector_field()
        text = Text(text = f"Minimum path spent {self.total_time} seconds")
        text.scale_to_fit_width(5.5)
        text.next_to(self.vf_streamLines, LEFT, buff=0.5)
        text.align_to(self.vf_streamLines, UP).shift(DOWN * 0.4)

        self.time_tracker = ValueTracker(0)
        self.boat = Dot(color=ORANGE, radius=0.1)
        self.boat.move_to(np.array([
            self.tx(0), 
            self.ty(0), 
            0
        ]))
        self.add(self.boat)

        self.boat.add_updater(self.move_boat)
        self.zoomed_camera.frame.add_updater(lambda cam: cam.move_to(self.boat.get_center()))

        self.play(Write(text))

        self.zoomed_display.next_to(text, DOWN, buff=0.4)
        self.activate_zooming(animate=True)

        self.play(
            self.time_tracker.animate.set_value(self.total_time),
            run_time = self.total_time/self.velocity_factor,
            rate_func = linear
        )


    def construct(self):

        self.find_track()

        if self.tx is None: self.create_no_path_animation()
        else: self.create_path_animation()

        self.wait(5)

class Trigonometric_field_simulation(Track_Simulation):
    vector_field_values = np.load('data/trigonometric_field.npy')

class Cavity_flow_simulation(Track_Simulation):
    vector_field_values = np.load('data/cavity_flow.npy')

class Channel_flow_simulation(Track_Simulation):
    vector_field_values = np.load('data/channel_flow.npy')
        
class Trigonometric_field_simulation_x2(Track_Simulation):
    vector_field_values = np.load('data/trigonometric_field.npy')
    velocity_factor=2

class Cavity_flow_simulation_x2(Track_Simulation):
    vector_field_values = np.load('data/cavity_flow.npy')
    velocity_factor=2

class Channel_flow_simulation_x2(Track_Simulation):
    vector_field_values = np.load('data/channel_flow.npy')
    velocity_factor=2
        
