import ctypes
import PIL
from PIL import Image
# noinspection PyUnresolvedReferences
from win32api import GetSystemMetrics
from PyQt5.QtCore import QTimer


class DesktopBackground:
    def __init__(self, image_dict, interval):
        # The path to the folder that contains the images that can be picked as the desktop background.
        self.image_dict = image_dict

        self.interval = interval

        self.timer = QTimer()
        self.timer.timeout.connect(self.background_changer)

    def background_changer(self):
        """
        Changes the background of the desktop to a random image from the self.image_dict folder.

        :return: None
        """
        # TODO: Maybe implement a system to ensure equal distribution of picks.
        # Choosing a random picture from the folder containing all possible backgrounds.

        # Resizing the image so it fits the desktop size.

        # Setting the background

    def set_background(self, image_name):
        image = Image.open(self.image_dict + image_name)

        image.save(self.image_dict + "background.jpg")

        ctypes.windll.user32.SystemParametersInfoW(20, 0, directory_path + "background.jpg", 0)

    # TODO: Make it so we resize through scaling instead of forcing width and height.
    @staticmethod
    def resize_image(image, width=GetSystemMetrics(0), height=GetSystemMetrics(1)):
        return image.resize((width, height))


directory_path = "C:/Users/chris/PycharmProjects/reddit-desktop-background/images/"
