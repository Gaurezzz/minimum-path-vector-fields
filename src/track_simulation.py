from manim import *
import numpy as np
from scipy.interpolate import RegularGridInterpolator, interp1d
from src.minimum_path_algorithm import Minimum_Path_Algorithm
from src.vector_field_functions.vector_field import VectorField
from src.vector_field_functions.gire import Gire

class Track_Simulation(ZoomedScene):
    """Base class for simulating and visualizing optimal pathfinding on vector fields using Manim.

    This class sets up a zoomed camera scene, calculates the minimum distance path across a vector field
    using the A* algorithm, and renders the animation of a particle (boat) navigating through the flow.
    Subclasses should inherit from this class and override the class attributes below to customize the simulation.

    Attributes:
        nx (int): Grid resolution along the x-axis used for pathfinding. Defaults to 100.
        ny (int): Grid resolution along the y-axis used for pathfinding. Defaults to 100.
        map_height (float): Visual height of the simulation field in Manim units. Defaults to 7.6.
        map_width (float): Visual width of the simulation field in Manim units. Defaults to 7.6.
        vector_field (VectorField): The vector field instance defining the flow velocities.
            MUST be defined in subclasses.
        velocity_factor (int | float): Speed multiplier for the animation playback. Defaults to 1.
        desired_arrows (int): Resolution of arrows/streamlines along each axis for visual rendering. Defaults to 25.
        initial_position_x (int): Starting grid index along the x-axis for the particle. Defaults to 1.
        initial_position_y (int): Starting grid index along the y-axis for the particle. Defaults to 1.
        final_position_x (int): Destination grid index along the x-axis for the particle. Defaults to 98.
        final_position_y (int): Destination grid index along the y-axis for the particle. Defaults to 98.
        steady (bool): If True, renders static streamlines for a time-independent flow.
            If False, dynamically redraws vector arrows over time for time-dependent flows. Defaults to True.
        particle_constant_velocity (float): Constant navigation speed of the particle/boat. Defaults to 10.
    """

    nx: int = 100
    ny: int = 100
    map_height: float = 7.6
    map_width: float = 7.6
    vector_field: VectorField
    velocity_factor = 1
    desired_arrows = 25
    initial_position_x: int = 1
    initial_position_y: int = 1
    final_position_x: int = 98
    final_position_y: int = 98
    steady: bool = True
    particle_constant_velocity: float = 10

    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoomed_display_width=5.4,
            zoomed_display_height=5.4,
            zoom_factor=0.35, 
            **kwargs
        )

    def create_vector_field(self):

        x_min, x_max, y_min, y_max = self.vector_field.get_limits()

        vf_manim_x_min = -0.75
        vf_manim_x_max = self.map_width - 0.75
        vf_manim_y_min = -3.8
        vf_manim_y_max = self.map_height - 3.8

        x_step = (vf_manim_x_max - vf_manim_x_min) / self.desired_arrows
        y_step = (vf_manim_y_max - vf_manim_y_min) / self.desired_arrows

        if not self.steady:
            self.vf_streamLines = always_redraw(
                lambda: ArrowVectorField(
                    func=lambda pos: np.array(
                        self.vector_field.get_point_by_position(
                        x = x_min + ((pos[0] + 0.75) / self.map_width) * (x_max - x_min),
                        y = y_min + ((pos[1] + 3.8) / self.map_height) * (y_max - y_min),
                        t = self.time_tracker.get_value()),   
                    ),
                    x_range=[vf_manim_x_min, vf_manim_x_max, x_step],
                    y_range=[vf_manim_y_min, vf_manim_y_max, y_step],
                    colors=['#06e1fe', '#0076d1', '#1d00ad'],
                    min_color_scheme_value=0,
                    max_color_scheme_value=self.vector_field.get_maximum_velocity()
                )
            )

        else:

            self.vf_streamLines = StreamLines(
                func=lambda pos: np.array([
                    *self.vector_field.get_point_by_position(
                        x = x_min + ((pos[0] + 0.75) / self.map_width) * (x_max - x_min),
                        y = y_min + ((pos[1] + 3.8) / self.map_height) * (y_max - y_min),
                        t = 0 
                    ),  
                    0.0 
                ]),
                x_range=[vf_manim_x_min, vf_manim_x_max, x_step],
                y_range=[vf_manim_y_min, vf_manim_y_max, y_step],
                z_range=[0,0,1],
                dt=0.5 / max(self.vector_field.get_maximum_velocity(), 1.0),
                colors=['#06e1fe', '#0076d1', '#1d00ad'],
                min_color_scheme_value=0,
                max_color_scheme_value=self.vector_field.get_maximum_velocity()
            )

            self.vf_streamLines.start_animation(warm_up=False, flow_speed=1.5*self.velocity_factor)


        self.add(self.vf_streamLines)

    def find_track(self):

        MPA = Minimum_Path_Algorithm(self.vector_field)

        track = MPA.A_star(
            initial_position_x=self.initial_position_x,
            initial_position_y=self.initial_position_y,
            final_position_x=self.final_position_x,
            final_position_y=self.final_position_y,
            particle_constant_velocity=self.particle_constant_velocity
            )

        if track is None: 
            self.tx = None
            self.ty = None
            return

        track['x'] = np.array(track['x']) / (self.nx - 1) * self.map_width - 0.75
        track['y'] = np.array(track['y']) / (self.ny - 1) * self.map_height - 3.8
        track['t'] = np.round(np.array(track['t']), 2)

        #Set time as a soft function
        self.tx = interp1d(track['t'], track['x'], kind='cubic', bounds_error=False, fill_value="extrapolate")
        self.ty = interp1d(track['t'], track['y'], kind='cubic', bounds_error=False, fill_value="extrapolate")
        self.tβ = interp1d(track['t'], track['β'], kind='cubic', bounds_error=False, fill_value="extrapolate")
        self.tu = interp1d(track['t'], track['u'], kind='cubic', bounds_error=False, fill_value="extrapolate")
        self.tv = interp1d(track['t'], track['v'], kind='cubic', bounds_error=False, fill_value="extrapolate")
        
        self.total_time = track['t'][-1]

    def create_no_path_animation(self):

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

        text = Text(text = f"Minimum path spent {self.total_time} seconds")
        text.scale_to_fit_width(5.5)
        text.next_to(self.vf_streamLines, LEFT, buff=0.5)
        text.align_to(self.vf_streamLines, UP).shift(DOWN * 0.4)

        self.add(text)

        #Destination
        self.destination = Circle(radius=0.2, color=ORANGE, fill_color=BLACK,fill_opacity=0.7)
        self.destination.move_to(np.array([
            self.tx(self.total_time), 
            self.ty(self.total_time), 
            0
        ]))
        self.add(self.destination)

        #Boat
        self.boat = Dot(color=ORANGE, radius=0.1)
        self.boat.move_to(np.array([
            self.tx(0), 
            self.ty(0), 
            0
        ]))
        self.add(self.boat)
        self.boat.add_updater(self.move_boat)

        #Arrows
        ratio = min(max(10 / self.vector_field.get_maximum_velocity(), 0), 1)
        longitude = 0.5 + ratio*0.5

        def get_boat_arrow():
            t = self.time_tracker.get_value()
            if t >= self.total_time: return VGroup()
            β = self.tβ(t)

            start = self.boat.get_center() + np.array([
                0.1*np.cos(β),
                0.1*np.sin(β),
                0])

            end = start + np.array([
                longitude*np.cos(β),
                longitude*np.sin(β),
                0])

            arr = Arrow(
                start = start,
                end = end,
                stroke_width=18,
                color=GREEN,
                buff=0,
                max_stroke_width_to_length_ratio=1000,
            )

            arr.tip.scale(2.5)

            magnitude1 = Text(f"{10.0} m/s", weight=BOLD, font_size=6)
            magnitude1.move_to(start+np.array([0.25 * np.cos(β), 0.25 * np.sin(β),0]))
            magnitude1.rotate(β)
            
            return VGroup(arr, magnitude1)

        boat_arrow = always_redraw(get_boat_arrow)

        def get_vf_arrow():
            t = self.time_tracker.get_value()
            if t >= self.total_time: return VGroup()
            u = self.tu(t)
            v = self.tv(t)

            θ = np.arctan2(v, u)
            m = np.sqrt(u ** 2 + v ** 2)

            ratio = min(max(m / self.vector_field.get_maximum_velocity(), 0), 1)
            longitude = 0.5 + ratio*0.5

            start = self.boat.get_center() + np.array([
                0.1*np.cos(θ),
                0.1*np.sin(θ),
                0])

            end = start + np.array([
                longitude*np.cos(θ),
                longitude*np.sin(θ),
                0])

            arr2 = Arrow(
                start = start,
                end = end,
                stroke_width=18,
                color=BLUE,
                buff=0,
                max_stroke_width_to_length_ratio=1000,
            )

            arr2.tip.scale(2.5)

            magnitude2 = Text(f"{np.round(m, 1)} m/s", weight=BOLD, font_size=6)
            magnitude2.move_to(start+np.array([0.25 * np.cos(θ), 0.25 * np.sin(θ),0]))
            magnitude2.rotate(θ)
            
            return VGroup(arr2, magnitude2)

        vf_arrow = always_redraw(get_vf_arrow)
        self.add(boat_arrow, vf_arrow)

        self.zoomed_camera.frame.add_updater(lambda cam: cam.move_to(self.boat.get_center()))
        self.zoomed_display.next_to(text, DOWN, buff=0.4)
        self.activate_zooming(animate=True)


    def construct(self):

        self.time_tracker = ValueTracker(0)
        self.create_vector_field()
        self.find_track()

        if self.tx is None: self.create_no_path_animation()
        else: self.create_path_animation()

        percentages = [0.1,0.9]

        accumulated_percentage = 0

        for percentage in percentages:
            accumulated_percentage += percentage
            time_per_preview = self.total_time * percentage
            preview_time_limit = self.total_time * accumulated_percentage

            self.play(
                self.time_tracker.animate.set_value(preview_time_limit),
                run_time = time_per_preview/self.velocity_factor,
                rate_func = linear
            )

        self.wait(5)

