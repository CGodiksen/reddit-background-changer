import sys
import json
from PyQt5.QtCore import QThreadPool
from PyQt5 import QtWidgets, uic, QtGui
from subreddit_model import SubredditModel
from background_changer import BackgroundChanger
from worker import Worker


# TODO: All images could be refreshed on startup to avoid "dead" images that no longer fit the configuration.
# TODO: The app should run on startup and run in the background.
# TODO: The app should be minimized to the system tray.
# TODO: Add a way to manually set a new random background through the system tray.
# TODO: Add an icon to the application that can also be used for the system tray.
class MainWindow(QtWidgets.QMainWindow):
    """
    Class for creating the main window that our reddit desktop background desktop app will run in.
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('mainwindow.ui', self)

        # Setting up the internal model that handles the list of subreddits.
        self.model = SubredditModel()
        self.load_subreddits()
        self.subredditView.setModel(self.model)

        # Connecting buttons to the corresponding functionality.
        self.addButton.clicked.connect(self.add)
        self.updateButton.clicked.connect(self.update_subreddit)
        self.deleteButton.clicked.connect(self.delete)

        # Updating the shown subreddit settings in the UI when a subreddit from the listView is selected.
        self.subredditView.selectionModel().selectionChanged.connect(self.update_settings)

        # Setting up the background changer that will change the background every x seconds, specified by the interval.
        self.background_changer = BackgroundChanger("C:/Users/chris/PycharmProjects/reddit-desktop-background/images/")

        # Updating the interval when the change frequency spin box is changed.
        self.changeFrequencySpinBox.valueChanged.connect(self.background_changer.set_interval)

        # Setting up the thread pool that will handle the threads that are created when getting images.
        self.threadpool = QThreadPool()

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

            # Adding the images corresponding to the new subreddit to the image folder.
            # This is done in a new thread to ensure that the GUI is responsive even when getting images.
            worker = Worker(self.model.get_images, (name, time_limit, number_of_images), "images/")
            self.threadpool.start(worker)

            # Adding the subreddit icon to the icon folder.
            self.model.get_icon(name, "icons/")

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
            self.model.delete_images(self.model.subreddits[index.row()][0], "images/")

            # Deleting the icon corresponding to the deleted subreddit from the image folder.
            self.model.delete_images(self.model.subreddits[index.row()][0], "icons/")

            # Getting the new configuration settings.
            new_name = self.subredditEdit.text()
            new_time_limit = self.timeComboBox.currentText()
            new_number_of_images = self.numberSpinBox.value()

            # Updating the currently selected subreddit and emits the change.
            self.model.subreddits[index.row()] = (new_name, new_time_limit, new_number_of_images)
            self.model.dataChanged.emit(index, index)

            # Adding the images corresponding to the new subreddit to the image folder.
            # This is done in a new thread to ensure that the GUI is responsive even when getting images.
            worker = Worker(self.model.get_images, (new_name, new_time_limit, new_number_of_images), "images/")
            self.threadpool.start(worker)

            # Adding the subreddit icon to the icon folder.
            self.model.get_icon(new_name, "icons/")

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
            self.model.delete_images(self.model.subreddits[index.row()][0], "images/")

            # Deleting the icon corresponding to the deleted subreddit from the image folder.
            self.model.delete_images(self.model.subreddits[index.row()][0], "icons/")

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
        with open("subreddits.json", "r") as subreddit_file:
            data = json.load(subreddit_file)
            self.model.subreddits = data

    def save_subreddits(self):
        """Simple function that saves the current internal list model into the persistent json file."""
        with open("subreddits.json", "w") as subreddit_file:
            json.dump(self.model.subreddits, subreddit_file)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('reddit_icon.PNG'))
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
