import ctypes
import os
import random
from PIL import Image
# noinspection PyUnresolvedReferences
from win32api import GetSystemMetrics
from PyQt5.QtCore import QTimer


class DesktopBackground:
    def __init__(self, image_dict, interval):
        # The path to the folder that contains the images that can be picked as the desktop background.
        self.image_dict = image_dict

        # TODO: Make it so the interval can be decided through the UI.
        self.interval = interval

        self.timer = QTimer()
        self.timer.timeout.connect(self.background_changer)
        self.timer.start(10000)

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
