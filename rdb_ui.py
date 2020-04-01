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
        self.subredditView.setModel(self.model)

        # Connecting buttons to the corresponding functionality.
        self.addButton.clicked.connect(self.add)
        self.updateButton.clicked.connect(self.update_subreddit)
        self.deleteButton.clicked.connect(self.delete)

        # Catching other signals
        self.subredditView.selectionChanged.connect()

        # TODO: Add a helper function that changes the shown configuration when a list item is selected.

    def add(self):
        """
        Takes configuration settings in subredditEdit, timeComboBox and numberSpinBox and adds a new subreddit
        to the internal model with that configuration.
        :return: None
        """
        pass

    def update_subreddit(self):
        """
        Updates the currently selected subreddit with the current configuration settings in subredditEdit,
        timeComboBox and numberSpinBox.
        :return: None
        """
        pass

    def delete(self):
        """
        Deletes the selected subreddit from the internal model.
        :return: None
        """
        pass

    def update_settings(self):
        """
        Updates the currently shown configuration settings when a new item is selected in the subredditView.
        :return: None
        """
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()