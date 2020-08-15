from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from shutil import copyfile
import praw
import json
import urllib.request
import os
import ctypes


class SubredditModel(QtCore.QAbstractListModel):
    """
    Class for creating an abstract list model that is subclassed to support a list of subreddits. This involves saving
    a list of tuples, with the format (name, time limit, picture limit).

    Here time limit describes the setting for "top" which can be "Now", "Today", "This week", "This month", "This year"
    and "All time". Picture limit describes how many pictures we want from the specific subreddit.

    The tuple (/r/aww, "this year", 25) would get the top 25 pictures within the last year from the subreddit /r/aww.
    """

    def __init__(self, main_window, subreddits=None, *args, **kwargs):
        super(SubredditModel, self).__init__()
        # The internal storage that will store configuration tuples.
        self.subreddits = subreddits or []

        # Getting the secret information for the reddit application from the config file.
        with open("configuration/reddit_config.json", "r") as config_file:
            config = json.load(config_file)

        # Creating the reddit instance using the secret information.
        self.reddit = praw.Reddit(client_id=config["client_id"], client_secret=config["client_secret"],
                                  user_agent=config["user_agent"])

        self.main_window = main_window
        self.settings = {}

        # Used for getting the monitor resolution.
        self.user32 = ctypes.windll.user32

    def data(self, QModelIndex, role=None):
        """
        Returns the data stored under the given role for the item referred to by the index.

        :param QModelIndex: The specific index of the model that we wish to extract data for.
        :param role: The specific data that we wish to extract.
        :return: The name of the subreddit if the role is DisplayRole.
        """
        name, _, _ = self.subreddits[QModelIndex.row()]

        if role == Qt.DisplayRole:
            return "/r/" + name

        # Inserting the subreddit icon before the name in each row.
        if role == Qt.DecorationRole:
            # Iterating through the icons.
            for filename in os.listdir("data/icons/"):
                # When we find the correct icon for the subreddit we return a scaled version.
                if filename.lower().startswith(name.lower()):
                    icon = QtGui.QImage("data/icons/" + filename)
                    return icon.scaled(25, 25)

    def rowCount(self, parent=None, *args, **kwargs):
        """
        Simple function that returns the total rowcount of the internal model representation. Since we use a list this
        is simply the length of the list.
        """
        return len(self.subreddits)

    def get_images(self, subreddit_config, save_path):
        """
        Uses PRAW to get the images from reddit that are described by the specific subreddit configuration. Once gotten
        the function saves them to the specified folder.

        :param save_path: The path to the folder in which we save the images.
        :param subreddit_config: The subreddit configuration that describes the subreddit we should search, the time limit
        the search should be within and the amount of images we should find.
        :return: None
        """
        # Incrementing getting_images since one more worker is getting images.
        self.main_window.getting_images += 1
        # Disabling the delete and update buttons since the application crashes if the user delete while getting images.
        self.main_window.deleteButton.setEnabled(False)
        self.main_window.updateButton.setEnabled(False)

        # Loading the settings from the app_settings json file to get the blacklist.
        self.load_settings()

        # Pulling the information from the configuration to increase readability.
        name, time_limit, number_of_images = subreddit_config

        # Converting the time limit into the corresponding time filter that can be used in top().
        time_limit = self.convert_time_limit(time_limit)

        subreddit = self.reddit.subreddit(name)
        image_counter = 0

        for submission in subreddit.top(time_filter=time_limit, limit=1000):
            # Ensuring that we only retrieve the requested amount of images.
            if image_counter == number_of_images:
                break

            # Catching rare problematic submissions and ignoring them if they cause problems.
            try:
                # Ensuring that we only download images and that the images are hosted on the reddit domain.
                if submission.is_reddit_media_domain and submission.is_video is False:
                    # Ensuring that the images are large enough to be used as a desktop background.
                    if submission.preview["images"][0]["source"]["width"] > self.user32.GetSystemMetrics(0) and \
                            submission.preview["images"][0]["source"]["height"] > self.user32.GetSystemMetrics(1):
                        filename = name + "_" + submission.name + ".jpg"
                        # If the filename is not in the blacklist.
                        if filename not in self.settings["blacklist"]:
                            # Downloading the image from the url and saving it to the folder using its unique name.
                            urllib.request.urlretrieve(submission.preview["images"][0]["source"]["url"],
                                                       save_path + filename)
                            image_counter += 1
            except Exception as e:
                print("Image getter:" + str(e))
                continue

        self.main_window.getting_images -= 1

        # Enabling the delete and update buttons again if there is no workers currently getting images.
        if self.main_window.getting_images == 0:
            self.main_window.deleteButton.setEnabled(True)
            self.main_window.updateButton.setEnabled(True)

    def get_all_images(self, save_path):
        """
        Finds the specified images for every subreddit configuration that is currently in the internal list model.

        :param save_path: The path to the folder in which we save the images.
        :return: None
        """
        for subreddit in self.subreddits:
            self.get_images(subreddit, save_path)

    @staticmethod
    def delete_images(subreddit_name, delete_path):
        """
        Deletes all images in the folder specified by the delete path that are from the given subreddit.

        :param subreddit_name: The subreddit which pictures should be removed from the delete path folder.
        :param delete_path: The folder in which we should delete the picture.
        :return: None
        """
        # Iterating through the files in the delete folder.
        for filename in os.listdir(delete_path):
            # If the file is from the given subreddit then we delete it.
            if filename.lower().startswith(subreddit_name.lower()):
                os.remove(os.path.join(delete_path, filename))

    @staticmethod
    def convert_time_limit(time_limit):
        """
        Converts the time limit from the combobox into the corresponding internal value that can be used in PRAW.

        :param time_limit: The time limit that we wish to convert.
        :return: The value that corresponds to the time_limit argument.
        """
        return {
            "Now": "hour",
            "Today": "day",
            "This week": "week",
            "This month": "month",
            "This year": "year",
            "All time": "all"
        }[time_limit]

    def get_icon(self, subreddit_name, save_path):
        """
        Saves the icon of the given subreddit to the folder specified by the save path argument.
        :param subreddit_name: The subreddit that we wish to find the icon of.
        :param save_path: The folder we should save the icon to.
        :return: None
        """
        subreddit = self.reddit.subreddit(subreddit_name)

        # If the subreddit has an icon.
        if subreddit.icon_img != "":
            # Save the icon to the icons folder.
            urllib.request.urlretrieve(subreddit.icon_img, save_path + subreddit.display_name + ".png")
        # If not we just save the subreddit icon as the default icon.
        else:
            copyfile("resources/default_subreddit_icon.png", save_path + subreddit.display_name + ".png")

    def load_settings(self):
        """Loading the settings from the settings file and return the dictionary."""
        with open("configuration/app_settings.json", "r") as subreddit_file:
            self.settings = json.load(subreddit_file)
