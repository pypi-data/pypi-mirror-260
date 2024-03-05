import cv2
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
import os

class WindowClass:
    def __init__(self, cam, width=480, height=320, window_name="Application"):

        """
        Windows Class to Create a Tkinter Window for Camera Stream.

        Attributes:
            cam: cv2.VideoCapture
                Camera Object to Stream Video
            width: int, default 480
                Width of the Window
            height: int, default 320
                Height of the Window
            window: tk.Tk
                Tkinter Window Object
            label: tk.Label
                Tkinter Label Object to Show Image
            thread: Thread
                Thread Object to Update Image in Realtime

        Returns:
            None
        """

        self.cam = cam
        self.width = width
        self.height = height
        self.window = tk.Tk()
        self.window.title(window_name)
        self.window.geometry(str(width) + "x" + str(height))
        self.label = tk.Label(self.window)
        self.label.pack()
        self.thread = Thread(target=self.viewfinder)
        self.thread.start()

    def viewfinder(self):

        """
        Function to Update Image in Realtime.

        Arguments:
            None

        Returns:
            None
        """

        while True:
            ret, frame = self.cam.read()
            if ret:
                frame = cv2.resize(frame, (self.width, self.height))
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                image = ImageTk.PhotoImage(image)
                self.label.config(image=image)
                self.label.image = image
                self.window.update()

    def run(self):

        """
        Function to Run Tkinter Window.

        Arguments:
            None

        Returns:
            None
        """

        self.window.mainloop()
        self.cam.release()
        os._exit(0)
