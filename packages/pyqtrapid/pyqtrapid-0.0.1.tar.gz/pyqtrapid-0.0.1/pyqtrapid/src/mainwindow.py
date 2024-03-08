import os
import sys
# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QLabel, QPushButton, QSpinBox, QTableWidget
# from PyQt5.QtGui import QFont, QPixmap
from PyQt5.uic import loadUiType

def get_resource_path(relative_path):
    """
    Get the absolute path to the resource based on whether the script is running as an executable or as a script.
    """
    if getattr(sys, 'frozen', False):
        # Running as an executable, use sys._MEIPASS to access bundled files
        base_path = sys._MEIPASS
    else:
        # Running as a script, use the script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    resource_path = os.path.join(base_path, relative_path)
    return resource_path

# Constants and configuration
APP_NAME = "MainWindow"
ui, _ = loadUiType(get_resource_path('../ui/mainwindow.ui'))

# Main application window
class MainWindow(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(APP_NAME)

    # Continue with your code
    ...


# Application entry point
def main():
    # Initialize the application
    app = QApplication(sys.argv)
    
    # Create and show the main window
    mainWindow = MainWindow()
    mainWindow.show()
    
    # Start the application event loop
    sys.exit(app.exec_())

# Entry point for standalone execution
if __name__ == "__main__":
    main()
