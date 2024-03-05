import cv2
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
import os


class WindowCamera:
    def __init__(self, cam, filename="captured_image.jpg", wide=480, high=320):

        """
        Windows Class to Create a Tkinter Window for Camera Stream.

        :argument
        cam: cv2.VideoCapture
            Camera Object to Stream Video
        wide: int, default 480
            Width of the Window
        high: int, default 320
            Height of the Window
        window: tk.Tk
            Tkinter Window Object
        label: tk.Label
            Tkinter Label Object to Show Image
        button_frame: tk.Frame
            Tkinter Frame Object to Place Button
        button_capture: tk.Button
            Tkinter Button Object to Capture Image
        thread: Thread
            Thread Object to Update Image in Realtime
        """

        self.cam = cam
        self.filename = filename
        self.wide = wide
        self.high = high
        self.window = tk.Tk()
        self.window.title("Model Inference App")
        self.window.geometry(str(wide) + "x" + str(high))
        self.label = tk.Label(self.window)
        self.label.pack()
        self.button_frame = tk.Frame(self.window)
        self.button_frame.place(relx=0.5, rely=0.9, anchor='center')
        self.button_capture = tk.Button(self.button_frame, text="Capture", command=lambda: self.capture_image())
        self.button_capture.pack(side="left", expand=True)
        self.thread = Thread(target=self.viewfinder)
        self.thread.start()
        self.window.mainloop()
        self.cam.release()
        os._exit(0)

    def viewfinder(self):

        """
        Function to Update Image in Realtime.

        :parameter
        None

        :return
        None
        """

        while True:
            ret, frame = self.cam.read()
            if ret:
                frame = cv2.resize(frame, (self.wide, self.high))
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                image = ImageTk.PhotoImage(image)
                self.label.config(image=image)
                self.label.image = image

    def capture_image(self):

        """
        Function to Capture Image from Camera.

        :parameter
        filename: str, default "captured_image.jpg"
            Name of the File to Save Image

        :return
        None
        """

        ret, frame = self.cam.read()
        if ret:
            frame = cv2.resize(frame, (self.wide, self.high))
            new_window = tk.Toplevel(self.window)
            new_label = tk.Label(new_window)
            new_label.pack()
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image = ImageTk.PhotoImage(image)
            new_label.config(image=image)
            new_label.image = image
            cv2.imwrite(self.filename, frame)
