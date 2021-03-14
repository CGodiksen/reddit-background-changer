import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWinExtras import QtWin

from reddit_background_changer.background_changer import BackgroundChanger
from reddit_background_changer.main_window import MainWindow
from reddit_background_changer.system_tray import SystemTray


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('../resources/reddit_icon.ico'))

    # Changing the app id so our custom window icon is shown on the toolbar.
    QtWin.setCurrentProcessExplicitAppUserModelID('reddit_background_changer.v1.0')

    # Ensuring that we do not stop the application when the main window is closed.
    app.setQuitOnLastWindowClosed(False)

    # Setting up the background changer that will be used in the main window and the system tray.
    # We use the absolute path since it is required when changing the background on windows.
    background_changer = BackgroundChanger()

    main_window = MainWindow(background_changer)
    system_tray = SystemTray(background_changer, main_window, app)

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
