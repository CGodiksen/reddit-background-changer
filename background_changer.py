import ctypes
import os
import random

from PyQt5.QtCore import QTimer

from settings import Settings


class BackgroundChanger:
    def __init__(self):
        # The filename of the image that is currently the desktop background.
        self.current_background = ""

        # The path to the folder that contains the images that can be picked as the desktop background.
        self.image_folder = os.path.abspath("data/images") + "/"

        self.settings = Settings()

        # Setting up the timer that changes the background to a random picture according to the time interval.
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_background)
        self.timer.start(self.settings.change_frequency * 60000)

        # Changing the background immediately since the application is launched on computer startup.
        self.change_background()

    def change_background(self):
        """Changes the background of the desktop to a random image from the self.image_dict folder."""
        # Wrapping in a try-except to handle invalid/broken images and the case where there are no images in the folder.
        try:
            # Choosing a random image from the folder containing all possible backgrounds.
            background_name = random.choice(os.listdir(self.image_folder))

            # Setting the new desktop background image to the chosen image.
            ctypes.windll.user32.SystemParametersInfoW(20, 0, self.image_folder + background_name, 0)

            self.current_background = background_name

            # Restarting the timer.
            self.timer.start(self.settings.change_frequency * 60000)
        except Exception as e:
            print("Background changer: " + str(e))

    def set_interval(self, interval_minutes):
        """Setter function for the interval instance variable that restarts the timer with the new interval."""
        # Multiplied by 60000 to convert minutes to ms.
        self.settings.change_frequency = interval_minutes
        self.timer.start(self.settings.change_frequency * 60000)

        # Saving the changed settings to the settings file.
        self.settings.save_settings()
