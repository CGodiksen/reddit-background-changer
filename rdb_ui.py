import sys

from PyQt5 import QtWidgets, QtGui

from background_changer import BackgroundChanger
from main_window import MainWindow
from system_tray import SystemTray


# TODO: All images could be refreshed on startup to avoid "dead" images that no longer fit the configuration.
# TODO: The app should run on startup and run in the background.
# TODO: Rename this file.
# TODO: Put the icon in a folder related to application images.
# TODO: Put all the json files in a folder containing data about the application.
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('resources/reddit_icon.PNG'))

    # Ensuring that we do not stop the application when the main window is closed.
    app.setQuitOnLastWindowClosed(False)

    # Setting up the background changer that will be used in the main window and the system tray.
    background_changer = BackgroundChanger("C:/Users/chris/PycharmProjects/reddit-desktop-background/images/")

    main_window = MainWindow(background_changer)
    system_tray = SystemTray(background_changer)

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
