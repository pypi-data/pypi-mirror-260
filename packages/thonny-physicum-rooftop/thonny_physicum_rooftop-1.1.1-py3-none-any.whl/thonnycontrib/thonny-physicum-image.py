import os
from tkinter import Label, ttk, messagebox
from thonny import get_workbench
from PIL import Image, ImageTk
import requests
from io import BytesIO
import socket

class Physicum(Label):
    def __init__(self, master):
        super().__init__(master)

        # Get the background color of the Thonny code editor
        style = ttk.Style()
        bg_color = style.lookup('Text', 'background')

        # Set the background color of the widget
        self.configure(background=bg_color)

        # Initialize the PhotoImage variable
        self.photo = None
        self.link = "https://meteo.physic.ut.ee/webcam/uus/suur.jpg"

        self.load_content()
        
    def is_internet_available(self):
        try:
            # Try to establish a connection to a well-known website (e.g., Google DNS)
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            return False

    def set_text(self, text):
        self.config(text=text)
        self.update()

    def load_content(self):
        # Check for internet connection before proceeding
        if not self.is_internet_available():
            self.set_text("No internet connection!\nCan't get the live feed.\n\nConnect to the internet and restart Thonny.")
            messagebox.showerror("Error", "No internet connection! Can't get the live feed.")
            return False
        
        # Function to fetch a new image from the URL
        def get_new_image():
            response = requests.get(self.link)
            return Image.open(BytesIO(response.content))

        # Function to update the frame
        def update_frame():
            image = get_new_image()

            # Resize the image to fit the Thonny window
            width, height = image.size
            new_width = 400
            new_height = int(height * (new_width / width))
            resized_image = image.resize((new_width, new_height))

            # Create PhotoImage here and assign it to the class variable
            self.photo = ImageTk.PhotoImage(resized_image)
            self.config(image=self.photo)
            self.after(60000, update_frame)  # Refresh every 1 minute

        # Start the animation
        update_frame()

def load_plugin():
    get_workbench().add_view(Physicum, "Physicum Rooftop", "e", default_position_key="zz")