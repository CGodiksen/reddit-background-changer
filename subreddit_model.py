import ctypes
import os
import urllib.request
from shutil import copyfile

import praw
import prawcore
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

from settings import Settings


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

        # Setting up the settings containing the secret information for the reddit instance and the blacklist.
        self.settings = Settings()

        self.main_window = main_window

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
        :param subreddit_config: The subreddit configuration that describes the subreddit we should search, the time
        limit the search should be within and the amount of images we should find.
        """
        # Loading the most recent settings.
        self.settings.load_settings()

        # Pulling the information from the configuration to increase readability.
        name, time_limit, number_of_images = subreddit_config

        # Creating the reddit instance using the secret information.
        reddit = praw.Reddit(client_id=self.settings.client_id, client_secret=self.settings.client_secret,
                             user_agent=self.settings.user_agent)

        # Stopping further execution of the method if the subreddit does not exist.
        if not self.check_subreddit_exists(reddit, subreddit_config):
            return

        subreddit = reddit.subreddit(name)

        # Incrementing getting_images since one more worker is getting images.
        self.main_window.getting_images += 1
        # Disabling the delete and update buttons since the application crashes if the user delete while getting images.
        self.main_window.deleteButton.setEnabled(False)
        self.main_window.updateButton.setEnabled(False)

        # Visually changing the buttons so it is clear that they are disabled.
        self.main_window.deleteButton.setFlat(True)
        self.main_window.updateButton.setFlat(True)

        # Converting the time limit into the corresponding time filter that can be used in top().
        time_limit = self.convert_time_limit(time_limit)

        image_counter = 0
        for submission in subreddit.top(time_filter=time_limit, limit=1000):
            # Ensuring that we only retrieve the requested amount of images.
            if image_counter == number_of_images:
                break

            # Catching rare problematic submissions and ignoring them if they cause problems.
            try:
                filename = name + "_" + submission.name + ".jpg"
                if self.check_background_viability(submission, filename):
                    # Downloading the image from the url and saving it to the folder using its unique name.
                    urllib.request.urlretrieve(submission.preview["images"][0]["source"]["url"], save_path + filename)
                    image_counter += 1
            except Exception as e:
                print("Image getter:" + str(e))
                continue

        # Adding the subreddit icon to the icon folder.
        self.get_icon(subreddit, "data/icons/")

        self.main_window.getting_images -= 1

        # Enabling the delete and update buttons again if there is no workers currently getting images.
        if self.main_window.getting_images == 0:
            self.main_window.deleteButton.setEnabled(True)
            self.main_window.updateButton.setEnabled(True)

            # Visually changing the buttons back so it is clear they are enabled again.
            self.main_window.deleteButton.setFlat(False)
            self.main_window.updateButton.setFlat(False)

    def check_background_viability(self, submission, filename):
        """
        Checks whether or not the given submission is viable to use as a desktop background. This includes checking that
        the submission is hosted on the reddit media domain, checking that the submission is an image, checking that
        the image is large enough, checking that the aspect ratio is similar to the monitor aspect ratio and finally
        checking if the image is in the blacklist.

        :param submission: The reddit submission that is checked for its viability as an background image.
        :param filename: The filename of the image if it was downloaded, used to check if the image is in the blacklist.
        :return: True if the submission is viable as a desktop background, false otherwise.
        """
        if submission.is_reddit_media_domain:
            if submission.is_video is False:
                image_width = submission.preview["images"][0]["source"]["width"]
                image_height = submission.preview["images"][0]["source"]["height"]
                monitor_width = ctypes.windll.user32.GetSystemMetrics(0)
                monitor_height = ctypes.windll.user32.GetSystemMetrics(1)

                if image_width >= monitor_width and image_height >= monitor_height:
                    image_aspect_ratio = image_width / image_height
                    monitor_aspect_ratio = monitor_width / monitor_height

                    if abs(monitor_aspect_ratio - image_aspect_ratio) <= 0.2:
                        if filename not in self.settings.blacklist:
                            return True
        return False

    @staticmethod
    def delete_images(subreddit_name):
        """
        Deletes all images from the background image pool that are from the given subreddit. Also deletes the
        subreddits icon from the icon folder.

        :param subreddit_name: The subreddit specifying what images and which icon that should be deleted.
        """
        # Deleting the images from the background image pool.
        for filename in os.listdir("data/images/"):
            if filename[:-14].lower() == subreddit_name.lower():
                os.remove(os.path.join("data/images/", filename))

        # Deleting the icon from the icon folder.
        for filename in os.listdir("data/icons/"):
            if filename[:-4].lower() == subreddit_name.lower():
                os.remove(os.path.join("data/icons/", filename))

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

    @staticmethod
    def get_icon(subreddit, save_path):
        """
        Saves the icon of the given subreddit to the folder specified by the save path argument.
        :param subreddit: The subreddit that we wish to find the icon of.
        :param save_path: The folder we should save the icon to.
        """
        # If the subreddit has an icon.
        if subreddit.icon_img != "":
            # Save the icon to the icons folder.
            urllib.request.urlretrieve(subreddit.icon_img, save_path + subreddit.display_name + ".png")
        # If not we just save the subreddit icon as the default icon.
        else:
            copyfile("resources/default_subreddit_icon.png", save_path + subreddit.display_name + ".png")

    def check_subreddit_exists(self, reddit, subreddit_config):
        """
        Checks if the given subreddit exists. If not it removes the subreddit from the internal model.

        :param reddit: The praw reddit instance used to access reddit.
        :param subreddit_config: The subreddit configuration that describes the subreddit we should search for.
        :return: True if the subreddits exists, otherwise false.
        """
        # Pulling the subreddit name from the configuration.
        name, _, _ = subreddit_config

        try:
            reddit.subreddits.search_by_name(name, exact=True)
        except prawcore.NotFound as e:
            print("Subreddit does not exist: " + str(e))

            # Removing the subreddit from the internal model.
            self.main_window.model.subreddits.remove(subreddit_config)
            self.main_window.model.layoutChanged.emit()
            self.main_window.save_subreddits()

            return False

        return True
