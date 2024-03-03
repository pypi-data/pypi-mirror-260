import os
import itertools
from tkinter import Label, ttk
from thonny import get_workbench
from PIL import Image, ImageTk

class MyPluginView(Label):
    def __init__(self, master):
        super().__init__(master)

        # Get the background color of the Thonny code editor
        style = ttk.Style()
        bg_color = style.lookup('Text', 'background')

        # Set the background color of the widget
        self.configure(background=bg_color)

        self.load_content()

    def load_content(self):
        # Load a gif
        base_path = os.path.dirname(os.path.realpath(__file__))
        gif_path = os.path.join(base_path, 'main.gif')
        gif = Image.open(gif_path)

        # Get the number of frames
        num_frames = gif.n_frames
        # Create an iterator over the range of frames
        frames = itertools.cycle(range(num_frames))

        # Function to update the frame
        def update_frame():
            frame = next(frames)
            gif.seek(frame)
            photo = ImageTk.PhotoImage(gif)
            self.config(image=photo)
            self.image = photo  # Keep a reference to the image to prevent it from being garbage collected
            self.after(20, update_frame)  # Adjust the delay as needed

        # Start the animation
        update_frame()

def load_plugin():
    get_workbench().add_view(MyPluginView, "Subway Surfers", "ne", default_position_key="zz")
