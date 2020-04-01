import sys
import json
from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    """
    Class for creating the main window that our reddit desktop background desktop app will run in.
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('mainwindow.ui', self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()