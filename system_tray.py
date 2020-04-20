from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SystemTray:
    """
    Class for creating the icon in the system tray that can be used to open the window and quickly change
    background manually.
    """
    def __init__(self, background_changer, main_window, app):
        self.background_changer = background_changer
        self.main_window = main_window
        self.app = app

        # Setting up the system tray icon itself.
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("resources/reddit_icon.ico"))
        self.tray.setVisible(True)

        # Creating the menu.
        self.menu = QMenu()

        # Opening the main window when the tray icon is double clicked. We only want to call show() if the activation
        # reason is 2, meaning that the icon was double clicked.
        self.tray.activated.connect(
            lambda activation_reason: self.main_window.show() if activation_reason == 2 else None)

        # Creating an action that opens the main window.
        self.open_window_action = QAction("Open")
        self.open_window_action.triggered.connect(self.main_window.show)
        self.menu.addAction(self.open_window_action)

        # Creating an action that exits the application
        self.exit_app_action = QAction("Exit")
        self.exit_app_action.triggered.connect(self.app.exit)
        self.menu.addAction(self.exit_app_action)

        # Separating the default actions and the application specific actions.
        self.menu.addSeparator()

        # Creating an action that changes the background manually and adding it to the menu of the tray icon.
        self.change_background_action = QAction("Change background")
        self.change_background_action.triggered.connect(self.background_changer.background_changer)
        self.menu.addAction(self.change_background_action)

        # Add the menu to the tray.
        self.tray.setContextMenu(self.menu)
