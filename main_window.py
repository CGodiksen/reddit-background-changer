import json
import os
import pathlib

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThreadPool

from settings_dialog import SettingsDialog
from subreddit_model import SubredditModel
from worker import Worker


class MainWindow(QtWidgets.QMainWindow):
    """
    Class for creating the main window that our reddit desktop background desktop app will run in.
    """
    def __init__(self, background_changer, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi("resources/mainwindow.ui", self)

        self.create_storage_setup()

        # Setting up the internal model that handles the list of subreddits.
        self.model = SubredditModel(self)
        self.load_subreddits()
        self.subredditView.setModel(self.model)

        # Connecting buttons to the corresponding functionality.
        self.addButton.clicked.connect(self.add)
        self.updateButton.clicked.connect(self.update_subreddit)
        self.deleteButton.clicked.connect(self.delete)

        # Used to restart the timer if the change frequency was changed in the settings.
        self.background_changer = background_changer

        self.settings_dialog = SettingsDialog(background_changer)
        self.settingsButton.clicked.connect(self.settings_dialog.show)

        # Updating the shown subreddit settings in the UI when a subreddit from the listView is selected.
        self.subredditView.selectionModel().selectionChanged.connect(self.update_settings)

        # Setting up the thread pool that will handle the threads that are created when getting images.
        self.threadpool = QThreadPool()

        # Number that keeps track of how many workers that are currently getting images from reddit.
        self.getting_images = 0

    def add(self):
        """
        Takes configuration settings in subredditEdit, timeComboBox and numberSpinBox and adds a new subreddit
        to the internal model with that configuration.

        :return: None
        """
        name = self.subredditEdit.text()
        time_limit = self.timeComboBox.currentText()
        number_of_images = self.numberSpinBox.value()

        # If there is something to add.
        if name != "" and number_of_images != 0:
            # Updating the model and emitting that the layout has been changed.
            self.model.subreddits.append((name, time_limit, number_of_images))
            self.model.layoutChanged.emit()

            # Clearing the configuration settings
            self.subredditEdit.clear()
            self.timeComboBox.setCurrentIndex(0)
            self.numberSpinBox.setValue(0)

            # Adding the images and icon corresponding to the new subreddit to the image folder.
            # This is done in a new thread to ensure that the GUI is responsive even when getting images.
            worker = Worker(self.model.get_images, (name, time_limit, number_of_images), "data/images/")
            self.threadpool.start(worker)

            self.save_subreddits()

    def update_subreddit(self):
        """
        Updates the currently selected subreddit with the current configuration settings in subredditEdit,
        timeComboBox and numberSpinBox.

        :return: None
        """
        # Ensuring that we do not crash if no index is selected.
        try:
            index = self.subredditView.selectedIndexes()[0]
        except Exception as e:
            print("Update button: " + str(e))
            return

        # If something is selected.
        if index:
            # Deleting the images corresponding to the old subreddit configuration from the image folder.
            self.model.delete_images(self.model.subreddits[index.row()][0], "data/images/")

            # Deleting the icon corresponding to the deleted subreddit from the image folder.
            self.model.delete_images(self.model.subreddits[index.row()][0], "data/icons/")

            # Getting the new configuration settings.
            new_name = self.subredditEdit.text()
            new_time_limit = self.timeComboBox.currentText()
            new_number_of_images = self.numberSpinBox.value()

            # Updating the currently selected subreddit and emits the change.
            self.model.subreddits[index.row()] = (new_name, new_time_limit, new_number_of_images)
            self.model.dataChanged.emit(index, index)

            # Adding the images and icon corresponding to the new subreddit to the image folder.
            # This is done in a new thread to ensure that the GUI is responsive even when getting images.
            worker = Worker(self.model.get_images, (new_name, new_time_limit, new_number_of_images), "data/images/")
            self.threadpool.start(worker)

            self.save_subreddits()

    def delete(self):
        """
        Deletes the selected subreddit from the internal model.

        :return: None
        """
        # Ensuring that we don't crash if no index is selected.
        try:
            index = self.subredditView.selectedIndexes()[0]
        except Exception as e:
            print("Delete button: " + str(e))
            return

        # If something is selected.
        if index:
            # Deleting the images corresponding to the deleted subreddit from the image folder.
            self.model.delete_images(self.model.subreddits[index.row()][0], "data/images/")

            # Deleting the icon corresponding to the deleted subreddit from the image folder.
            self.model.delete_images(self.model.subreddits[index.row()][0], "data/icons/")

            # Deleting the subreddit from the internal list model and emitting the layout change.
            del self.model.subreddits[index.row()]
            self.model.layoutChanged.emit()

            self.save_subreddits()

    def update_settings(self):
        """
        Updates the currently shown configuration settings when a new item is selected in the subredditView.

        :return: None
        """
        index = self.subredditView.selectedIndexes()[0]

        # If something is selected.
        if index:
            # Getting the settings for the selected index.
            name, time_limit, number_of_images = self.model.subreddits[index.row()]

            # Setting the shown configuration settings to the settings for the selected index.
            self.subredditEdit.setText(name)
            self.timeComboBox.setCurrentIndex(self.timeComboBox.findText(time_limit))
            self.numberSpinBox.setValue(number_of_images)

    def load_subreddits(self):
        """Simple function that loads the data from the persistent json file into the internal list model."""
        with open("data/subreddits.json", "r") as subreddit_file:
            data = json.load(subreddit_file)
            self.model.subreddits = data

    def save_subreddits(self):
        """
        Simple function that saves the current internal list model into the persistent json file. If the json file
        does not exist then the file is created first.
        """
        with open("data/subreddits.json", "w") as subreddit_file:
            json.dump(self.model.subreddits, subreddit_file)

    @staticmethod
    def create_storage_setup():
        """
        Sets up the initial folder structure if it does not already exist. This includes creating a "data" folder
        that contains the two sub-folders "icons"  and "images". The "data" folder will also contain the "subreddits"
        json file which keeps track of the currently chosen added subreddits.
        """
        pathlib.Path("data/icons").mkdir(parents=True, exist_ok=True)
        pathlib.Path("data/images").mkdir(parents=True, exist_ok=True)

        if "subreddits.json" not in os.listdir("data"):
            with open("data/subreddits.json", "w+") as subreddit_file:
                json.dump([], subreddit_file)
