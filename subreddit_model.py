from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
import praw
import json
import pprint


class SubredditModel(QtCore.QAbstractListModel):
    """
    Class for creating an abstract list model that is subclassed to support a list of subreddits. This involves saving
    a list of tuples, with the format (name, time limit, picture limit).

    Here time limit describes the setting for "top" which can be "Now", "Today", "This week", "This month", "This year"
    and "All time". Picture limit describes how many pictures we want from the specific subreddit.

    The tuple (/r/aww, "this year", 25) would get the top 25 pictures within the last year from the subreddit /r/aww.
    """

    def __init__(self, *args, subreddits=None, **kwargs):
        super(SubredditModel, self).__init__()
        # The internal storage that will store configuration tuples.
        self.subreddits = subreddits or []

    def data(self, QModelIndex, role=None):
        """
        Returns the data stored under the given role for the item referred to by the index.
        :param QModelIndex: The specific index of the model that we wish to extract data for.
        :param role: The specific data that we wish to extract.
        :return: The name of the subreddit if the role is DisplayRole.
        """
        if role == Qt.DisplayRole:
            name, _, _ = self.subreddits[QModelIndex.row()]
            return "/r/" + name

    def rowCount(self, parent=None, *args, **kwargs):
        """
        Simple function that returns the total rowcount of the internal model representation. Since we use a list this
        is simply the length of the list.
        """
        return len(self.subreddits)

    def get_images(self, subreddit, save_path):
        """
        Uses PRAW to get the images from reddit that are described by the specific subreddit configuration. Once gotten
        the function saves them to the specified folder.
        :param save_path: The path to the folder in which we save the images.
        :param subreddit: The subreddit configuration that describes the subreddit we should search, the time limit
        the search should be within and the amount of images we should find.
        :return: None
        """
        # Getting the secret information for the reddit application from the config file.
        with open("config.json", "r") as config_file:
            config = json.load(config_file)

        reddit = praw.Reddit(client_id=config["client_id"], client_secret=config["client_secret"],
                             user_agent=config["user_agent"])

        subreddit = reddit.subreddit('aww')

        for submission in subreddit.hot(limit=10):
            if submission.is_reddit_media_domain and submission.is_video is False:
                print(submission.preview["images"][0]["source"])
                print(submission.preview["images"][0]["source"]["width"])
                print(submission.preview["images"][0]["source"]["height"])
                print(submission.preview["images"][0]["source"]["url"])

    def get_all_images(self, save_path):
        """
        Finds the specified images for every subreddit configuration that is currently in the internal list model.
        :param save_path: The path to the folder in which we save the images.
        :return: None
        """


testing = SubredditModel()

testing.get_images(None, None)
