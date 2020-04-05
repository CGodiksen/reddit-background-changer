import ctypes
import os
import random
import json
from PIL import Image
# noinspection PyUnresolvedReferences
from win32api import GetSystemMetrics
from PyQt5.QtCore import QTimer


class BackgroundChanger:
    def __init__(self, image_dict):
        # The path to the folder that contains the images that can be picked as the desktop background.
        self.image_dict = image_dict

        # Setting up the settings specific to the functionality that changes the background.
        self.settings = {}
        self.load_settings()

        # Setting up the timer that changes the background to a random picture according to the time interval.
        self.timer = QTimer()
        self.timer.timeout.connect(self.background_changer)
        self.timer.start(self.settings["interval"] * 1000)

    def background_changer(self):
        """
        Changes the background of the desktop to a random image from the self.image_dict folder.

        :return: None
        """
        # TODO: Maybe implement a system to ensure equal distribution of picks.
        # Choosing a random picture from the folder containing all possible backgrounds.
        background_name = random.choice(os.listdir(self.image_dict))

        background_image = Image.open(self.image_dict + background_name)
        # Resizing the image so it fits the desktop size.
        resized_background_image = self.resize_image(background_image)

        # Setting the background
        self.set_background(resized_background_image)

    def set_background(self, image):
        """Sets the desktop background to the given image."""
        image.save(self.image_dict + "background.jpg")

        ctypes.windll.user32.SystemParametersInfoW(20, 0, self.image_dict + "background.jpg", 0)

    # TODO: Make it so we resize through scaling instead of forcing width and height.
    @staticmethod
    def resize_image(image, width=GetSystemMetrics(0), height=GetSystemMetrics(1)):
        """Resizes the given image according to the given arguments."""
        return image.resize((width, height))

    def set_interval(self, interval_minutes):
        """Setter function for the interval instance variable that restarts the timer with the new interval."""
        # Multiplied by 60000 to convert minutes to ms.
        self.settings["interval"] = interval_minutes
        self.timer.start(self.settings["interval"] * 1000)

        # Saving the changed settings to the settings file.
        self.save_settings()

    def load_settings(self):
        """Loading the settings from the settings file and return the dictionary."""
        with open("settings.json", "r") as subreddit_file:
            self.settings = json.load(subreddit_file)

    def save_settings(self):
        """Saving the settings to the settings file."""
        with open("settings.json", "w") as subreddit_file:
            json.dump(self.settings, subreddit_file)