import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from widgets import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    executable = MainWindow()
    executable.show()


    sys.exit(app.exec())