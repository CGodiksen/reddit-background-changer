from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# TODO: The app should be minimized to the system tray.
# TODO: Add comments.
class SystemTray:
    def __init__(self, background_changer):
        self.background_changer = background_changer

        # Setting up the system tray functionality.
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("resources/reddit_icon.PNG"))
        self.tray.setVisible(True)

        # Create the menu.
        self.menu = QMenu()
        self.change_background_action = QAction("Change background")
        # TODO: Potential problem here. The function does not restart the timer.
        self.change_background_action.triggered.connect(self.background_changer.background_changer)
        self.menu.addAction(self.change_background_action)

        # Add the menu to the tray.
        self.tray.setContextMenu(self.menu)

        self.tray.show()
