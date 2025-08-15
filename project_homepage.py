import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget,
)
from matplotlib.backends.backend_qt5agg import FigureCanvas

#Import created classes
from homepage_widget import HomePageWidget
from datapage_widget import DataPageWidget
from preprocessingpage_widget import PreprocessingPageWidget
from mlpage_widget import MLPageWidget
from visualization_widget import VisualizationPageWidget
from Backend.data_backend import get_project_info, enumerate_progress

class ProjectWindow(QMainWindow):
    def __init__(self, project_filepath):    #These parameters will be passed from the menu-page (currently main.py)
        super().__init__()
        project_data = get_project_info(project_filepath)
        self.project_name = project_data['project_name']
        self.progress = enumerate_progress(project_data)
        self.setWindowTitle(f"Project: {self.project_name}")
        self.setGeometry(100, 100, 800, 600)

        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add Home tab
        self.home_page = HomePageWidget(project_filepath) #Calls the class from homepage_widget.py
        self.tabs.addTab(self.home_page, "Home")
        self.home_page.saveRequested.connect(self.home_page.show_save_message)    #Connects the messagebox confirming progress was saved to the save button

        # Add Data tab
        self.data_page = DataPageWidget()   #Guess which file this is calling the class form [Rolls Eyes]
        self.tabs.addTab(self.data_page, "Data Management")
        self.data_page.uploadRequested.connect(self.data_page.on_upload_eeg)
        self.data_page.livestreamRequested.connect(self.data_page.on_livestream_eeg)

        #Add Preprocessing Tab
        self.preprocessing_page = PreprocessingPageWidget()
        self.tabs.addTab(self.preprocessing_page, "Preprocessing")
        self.preprocessing_page.preprocessRequested.connect(self.preprocessing_page.on_preprocess)

        #Add Ml/Deep Learning Tab
        self.ml_deeplearning_page = MLPageWidget()
        self.tabs.addTab(self.ml_deeplearning_page, "ML/Deep Learning")

        #Add Visualization Tab
        self.visualization_page = VisualizationPageWidget()
        self.tabs.addTab(self.visualization_page, "Visualization")

        # Add other tabs
        self.tabs.addTab(self.create_pubish_page(), "Share/Publish")

    #Temporary functions for pages
    def create_pubish_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Share your creations for others to use!"))
        layout.addWidget(QPushButton("Upload Dataset"))
        layout.addWidget(QPushButton("Upload AI algorithm"))
        widget.setLayout(layout)
        return widget


