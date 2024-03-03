import ipywidgets as widgets
from IPython.display import display, clear_output
import threading
import time


class NBAnim:
    """
    A class for displaying and controlling a sequence of images as an animation within a Jupyter Notebook.

    Parameters
    ----------
    frames : list of str
        A list of file paths to the frames (images) to be displayed in the animation.
    animation_speed : float, optional
        The speed of the animation in seconds per frame. Default is 0.5 seconds.

    Attributes
    ----------
    frames : list of str
        Sorted list of frames to be animated.
    current_frame : int
        The index of the current frame being displayed.
    is_playing : bool
        Flag indicating whether the animation is currently playing.
    animation_speed : float
        The speed of the animation in seconds per frame.
    play_button : widgets.Button
        Button widget for playing the animation.
    pause_button : widgets.Button
        Button widget for pausing the animation.
    next_button : widgets.Button
        Button widget for moving to the next frame.
    previous_button : widgets.Button
        Button widget for moving to the previous frame.
    stop_button : widgets.Button
        Button widget for stopping the animation and resetting to the first frame.
    speed_slider : widgets.FloatSlider
        Slider widget for adjusting the animation speed.
    frame_display : widgets.Output
        Output widget for displaying the current frame.
    """

    def __init__(self, frames, animation_speed=0.5):
        self.frames = sorted(frames)
        self.current_frame = 0
        self.is_playing = False
        self.animation_speed = animation_speed

        self.play_button = widgets.Button(description="Play")
        self.pause_button = widgets.Button(description="Pause")
        self.next_button = widgets.Button(description="Next")
        self.previous_button = widgets.Button(description="Previous")
        self.stop_button = widgets.Button(description="Stop")
        self.speed_slider = widgets.FloatSlider(
            value=animation_speed, min=0.1, max=2.0, step=0.1, description="Speed:"
        )
        self.frame_display = widgets.Output()

        self.setup_widgets()
        self.display_controls()

    def setup_widgets(self):
        """Set up event handlers for the widget controls."""
        self.play_button.on_click(self.on_play_button_clicked)
        self.pause_button.on_click(self.on_pause_button_clicked)
        self.stop_button.on_click(self.on_stop_button_clicked)
        self.next_button.on_click(self.on_next_button_clicked)
        self.previous_button.on_click(self.on_previous_button_clicked)
        self.speed_slider.observe(self.on_speed_slider_change, names="value")

    def display_controls(self):
        """Display the animation controls and frame display widget."""
        controls = widgets.HBox(
            [
                self.play_button,
                self.pause_button,
                self.stop_button,
                self.previous_button,
                self.next_button,
                self.speed_slider,
            ]
        )
        display(controls)
        display(self.frame_display)

    def update_frame(self, frame_number):
        """
        Update the displayed frame.

        Parameters
        ----------
        frame_number : int
            The index of the frame to display.
        """
        with self.frame_display:
            clear_output(wait=True)
            with open(self.frames[frame_number], "rb") as file:
                image = file.read()
            display(widgets.Image(value=image, format="png"))

    def play_animation(self):
        """Play the animation from the current frame."""
        self.is_playing = True
        while self.is_playing and self.current_frame < len(self.frames):
            self.update_frame(self.current_frame)
            time.sleep(self.animation_speed)
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0

    def on_play_button_clicked(self, b):
        """Handle the play button click event."""
        if not self.is_playing:
            threading.Thread(target=self.play_animation).start()

    def on_pause_button_clicked(self, b):
        """Handle the pause button click event."""
        self.is_playing = False

    def on_stop_button_clicked(self, b):
        """Handle the stop button click event, stopping the animation and resetting to the first frame."""
        self.is_playing = False
        self.current_frame = 0
        self.update_frame(self.current_frame)

    def on_next_button_clicked(self, b):
        """Handle the next button click event, moving to the next frame."""
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.update_frame(self.current_frame)

    def on_previous_button_clicked(self, b):
        """Handle the previous button click event, moving to the previous frame."""
        self.current_frame = (self.current_frame - 1) % len(self.frames)
        self.update_frame(self.current_frame)

    def on_speed_slider_change(self, change):
        """
        Handle changes to the speed slider.

        Parameters
        ----------
        change : dict
            A dictionary containing details about the change.
        """
        self.animation_speed = change["new"]
