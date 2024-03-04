import os
import time
import itertools
import tkinter as tk
from tkinter import ttk, messagebox
from thonny import get_workbench
from PIL import Image, ImageTk
from urllib.request import urlopen, urlretrieve
import threading
import queue
import socket

class MyPluginView(tk.Label):
    def __init__(self, master):
        super().__init__(master)

        # Get the background color of the Thonny code editor
        style = ttk.Style()
        bg_color = style.lookup('Text', 'background')

        # Set the background color of the widget
        self.configure(background=bg_color)

        # Initialize instance variables for download progress
        self.total_size = 0
        self.progress = 0

        self.load_content()

    def is_internet_available(self):
        try:
            # Try to establish a connection to a well-known website (e.g., Google DNS)
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            return False

    def download_gif(self, gif_url, destination_path, progress_queue):
        # Notify the user that the download is starting
        self.set_text("Downloading media file. This may take 2.5-10 minutes.\nThis process only happens once.")

        # Download the gif from the given URL to the destination path
        with urlopen(gif_url) as response, open(destination_path, 'ab') as output_file:
            self.total_size = int(response.headers.get('Content-Length', 0))
            block_size = 8192

            while True:
                data = response.read(block_size)
                if not data:
                    break

                output_file.write(data)
                self.progress += len(data)
                percent_complete = (self.progress / self.total_size) * 100

                # Notify progress to the user
                progress_queue.put(percent_complete)

    def set_text(self, text):
        self.config(text=text)
        self.update()

    def load_content_async(self):
        base_path = os.path.dirname(os.path.realpath(__file__))
        gif_path = os.path.join(base_path, 'main.gif')

        if not os.path.exists(gif_path):
            # Check for internet connection before proceeding
            if not self.is_internet_available():
                self.set_text("No internet connection!\nCan't download the media file for Subway Surfers.\n\nConnect to the internet and restart Thonny.\n\nMedia download only happens once.")
                messagebox.showerror("Error", "No internet connection! Can't download the media file for Subway Surfers.")
                return False
            
            #gif_url = 'https://www.dropbox.com/scl/fi/5iqugjg7wdu5d65s2mobc/main.gif?rlkey=snekjxb32qho2tkh73v9a5rl0&dl=1'
            gif_url = 'https://download1529.mediafire.com/8w777hol8vkgVGJUY0_kjBc-agnlWo66fmSadT4D6lTC_25JMEzErguTQgEHGC_AulqL8dH5c0BbHn7QGYaEh0uaVsGxsxUfZTv2RlzJsWAch7JRCd3o4p48xVQhBgdkZukFEylrTPMRaysIz57JnXIdbNBHvC_JjyCxqYulQEKCSA/g8bs4y3g4tj8bx6/main.gif'

            progress_queue = queue.Queue()

            # Create a separate thread for the download
            download_thread = threading.Thread(target=self.download_gif, args=(gif_url, gif_path, progress_queue))
            download_thread.start()

            # Poll the progress queue and update the user
            while download_thread.is_alive():
                try:
                    percent_complete = progress_queue.get_nowait()
                    self.set_text(f"Downloading media file. This may take 2.5-10 minutes.\nThis process only happens once.\n\nDownload Progress: {percent_complete:.2f}%\n(The progress is not correct,\nit is just here to make it look more professional :D)")
                except queue.Empty:
                    pass
                self.update()
                self.after(1)  # Adjust the polling interval as needed (e.g., 100 milliseconds)

            # Download complete, reset the label text
            self.set_text("")

            # Show completion notification in a popup
            messagebox.showinfo('Download Complete', 'Media file download is complete. :)')

        # Load the downloaded gif
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
            self.after(20, update_frame)

        # Start the animation
        update_frame()

    def load_content(self):
        # Start the asynchronous-like download and loading
        self.after(0, self.load_content_async)

def load_plugin():
    get_workbench().add_view(MyPluginView, "Subway Surfers", "ne", default_position_key="zz")
