import sys
import json
from PyQt5 import QtWidgets, uic
from subreddit_model import SubredditModel


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
        self.load()
        self.subredditView.setModel(self.model)

        # Connecting buttons to the corresponding functionality.
        self.addButton.clicked.connect(self.add)
        self.updateButton.clicked.connect(self.update_subreddit)
        self.deleteButton.clicked.connect(self.delete)

        # Catching other signals.
        self.subredditView.selectionModel().selectionChanged.connect(self.update_settings)

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
            self.model.get_images((name, time_limit, number_of_images), "images/")

            # Adding the subreddit icon to the icon folder.
            self.model.get_icon(name, "icons/")

            self.save()

    def update_subreddit(self):
        """
        Updates the currently selected subreddit with the current configuration settings in subredditEdit,
        timeComboBox and numberSpinBox.

        :return: None
        """
        index = self.subredditView.selectedIndexes()[0]

        # If something is selected.
        if index:
            # Deleting the images corresponding to the old subreddit configuration from the image folder.
            self.model.delete_images(self.model.subreddits[index.row()], "images/")

            # Getting the new configuration settings.
            new_name = self.subredditEdit.text()
            new_time_limit = self.timeComboBox.currentText()
            new_number_of_images = self.numberSpinBox.value()

            # Updating the currently selected subreddit and emits the change.
            self.model.subreddits[index.row()] = (new_name, new_time_limit, new_number_of_images)
            self.model.dataChanged.emit(index, index)

            # Adding the images corresponding to the updated subreddit to the image folder.
            self.model.get_images((new_name, new_time_limit, new_number_of_images), "images/")

            # Adding the subreddit icon to the icon folder.
            self.model.get_icon(new_name, "icons/")

            self.save()

    def delete(self):
        """
        Deletes the selected subreddit from the internal model.

        :return: None
        """
        index = self.subredditView.selectedIndexes()[0]

        # If something is selected.
        if index:
            # Deleting the images corresponding to the deleted subreddit from the image folder.
            self.model.delete_images(self.model.subreddits[index.row()], "images/")

            # Deleting the subreddit from the internal list model and emitting the layout change.
            del self.model.subreddits[index.row()]
            self.model.layoutChanged.emit()

            self.save()

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

    def load(self):
        """
        Simple function that loads the data from the persistent json file into the internal list model.
        """
        with open("subreddits.json", "r") as subreddit_file:
            data = json.load(subreddit_file)
            self.model.subreddits = data

    def save(self):
        """
        Simple function that saves the current internal list model into the persistent json file.
        """
        with open("subreddits.json", "w") as subreddit_file:
            json.dump(self.model.subreddits, subreddit_file)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
