import sys

from PyQt5 import QtWidgets, QtGui

from background_changer import BackgroundChanger
from main_window import MainWindow
from system_tray import SystemTray


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('resources/reddit_icon.PNG'))

    # Ensuring that we do not stop the application when the main window is closed.
    app.setQuitOnLastWindowClosed(False)

    # Setting up the background changer that will be used in the main window and the system tray.
    background_changer = BackgroundChanger("C:/Users/chris/PycharmProjects/reddit-desktop-background/data/images/")

    main_window = MainWindow(background_changer)
    system_tray = SystemTray(background_changer, main_window, app)

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
