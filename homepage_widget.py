from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QLineEdit, QMessageBox, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas

#Import created classes
from progressbar_widget import ProgressBarWidget

# Custom widget for the homepage
class HomePageWidget(QWidget):
    saveRequested = pyqtSignal()

    def __init__(self, project_name, progress, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Project name label, centered
        name_label = QLabel(project_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont("Arial", 25))
        layout.addWidget(name_label)

        # Progress bar spanning the width
        progress_bar = ProgressBarWidget(progress)
        layout.addWidget(progress_bar)

        # Project description section
        project_description_label = QLabel("Write a more detailed description of your project:")
        layout.addWidget(project_description_label)

        project_description = QTextEdit()
        layout.addWidget(project_description)

        # Save button for project description
        save_description_button = QPushButton("Save Description")
        save_description_button.clicked.connect(self.saveRequested)
        layout.addWidget(save_description_button)

        # Project Metadata section
        project_metadata_label = QLabel("Project Metadata:")
        layout.addWidget(project_metadata_label)

        # Form layout for metadata fields
        metadata_layout = QFormLayout()

        # Project creation date (read-only for now)
        creation_date = "Lorem Ipsum"  # Dummy value, replace with actual data
        project_creation_date = QLabel(creation_date)
        metadata_layout.addRow("Project Created On:", project_creation_date)

        # Data/file used
        data_used = "cant believe im doing ts sober"
        project_data_used = QLabel(data_used)
        metadata_layout.addRow("File Used:", project_data_used)

        # Preprocessing methods
        preprocessing_methods_used = "Kill me"  # Dummy value
        preprocessing_used_label = QLabel(preprocessing_methods_used)
        metadata_layout.addRow("Preprocessing Methods Used:", preprocessing_used_label)

        # ML model used
        ml_model_used = "iuagiawergiUV"  # Dummy value
        ml_model_used_label = QLabel(ml_model_used)
        metadata_layout.addRow("ML/AI Model Used:", ml_model_used_label)

        # Project contributors
        project_contributors_label = QLabel("Project Contributors:")
        project_contributors = QLineEdit("Enter Names of Contributors separated by commas")
        save_contributors_button = QPushButton("Save")
        metadata_layout.addRow(project_contributors_label, self.create_field_with_save(project_contributors, save_contributors_button))

        layout.addLayout(metadata_layout)

        # Run Pipeline button
        run_button = QPushButton("Run Pipeline")
        layout.addWidget(run_button)

        self.setLayout(layout)

    def create_field_with_save(self, field, save_button):
        """Helper method to create a horizontal layout with a field and a save button."""
        h_layout = QHBoxLayout()
        h_layout.addWidget(field)
        h_layout.addWidget(save_button)
        save_button.clicked.connect(self.saveRequested)
        return h_layout
    
    #Home Page Functions
    def show_save_message(self):
        """Show a message box indicating that data has been saved."""
        msg_box = QMessageBox()
        msg_box.setText("Data saved")
        msg_box.setWindowTitle("Save Confirmation")
        msg_box.exec_()