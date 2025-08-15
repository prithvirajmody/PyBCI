from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QLineEdit, QMessageBox, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas

#Import created classes
from progressbar_widget import ProgressBarWidget
from Backend.data_backend import get_project_info, enumerate_progress, list_to_comma_string, set_project_info

# Custom widget for the homepage
class HomePageWidget(QWidget):
    saveRequested = pyqtSignal()

    def __init__(self, project_json_filepath, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        project_data = get_project_info(project_json_filepath)

        # Project name label, centered
        project_name = project_data['project_name']
        name_label = QLabel(project_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont("Arial", 25))
        layout.addWidget(name_label)

        # Progress bar spanning the width
        progress = enumerate_progress(project_data)
        progress_bar = ProgressBarWidget(progress)
        layout.addWidget(progress_bar)

        # Project description section
        project_description_label = QLabel("Write a more detailed description of your project:")
        layout.addWidget(project_description_label)

        project_description = QTextEdit()
        description = project_data['project_description']
        project_description.setPlainText(description)
        layout.addWidget(project_description)

        # Save button for project description
        save_description_button = QPushButton("Save Description")
        save_description_button.clicked.connect(lambda: self.save_description(project_json_filepath, project_description.toPlainText()))
        layout.addWidget(save_description_button)

        # Project Metadata section
        project_metadata_label = QLabel("Project Metadata:")
        layout.addWidget(project_metadata_label)

        # Form layout for metadata fields
        metadata_layout = QFormLayout()

        # Project creation date (read-only for now)
        creation_date = project_data['creation_date']
        project_creation_date = QLabel(creation_date)
        metadata_layout.addRow("Project Created On (yyyy-mm-dd):", project_creation_date)

        # Data/file used
        json_data_used = project_data['project_files']
        data_used = list_to_comma_string(json_data_used)
        project_data_used = QLabel(data_used)
        metadata_layout.addRow("File Used:", project_data_used)

        # Preprocessing methods
        json_preprocessing_data = project_data['preprocessing_settings']
        preprocessing_methods_used = list_to_comma_string(json_preprocessing_data)
        preprocessing_used_label = QLabel(preprocessing_methods_used)
        metadata_layout.addRow("Preprocessing Methods Used:", preprocessing_used_label)

        # ML model used
        json_ai_data = project_data['ai_algorithms']
        ml_model_used = list_to_comma_string(json_ai_data)
        ml_model_used_label = QLabel(ml_model_used)
        metadata_layout.addRow("ML/AI Model Used:", ml_model_used_label)

        # Project contributors
        project_contributors_label = QLabel("Project Contributors:")
        contributors = project_data['project_contributors']
        if len(contributors) == 0:
            self.project_contributors = QLineEdit("Enter Names of Contributors separated by commas")
        else:
            contributor_str = list_to_comma_string(contributors)
            self.project_contributors = QLineEdit(contributor_str)
        save_contributors_button = QPushButton("Save")
    
        metadata_layout.addRow(project_contributors_label, self.create_field_with_save(self.project_contributors, save_contributors_button, project_json_filepath))

        layout.addLayout(metadata_layout)

        # Run Pipeline button
        run_button = QPushButton("Run Pipeline")
        layout.addWidget(run_button)

        self.setLayout(layout)

    def create_field_with_save(self, field, save_button, json_filepath):
        """Helper method to create a horizontal layout with a field and a save button."""
        h_layout = QHBoxLayout()
        h_layout.addWidget(field)
        h_layout.addWidget(save_button)
        save_button.clicked.connect(lambda: self.save_contributors(json_filepath))
        return h_layout
    
    #Home Page Functions
    def show_save_message(self):
        """Show a message box indicating that data has been saved."""
        msg_box = QMessageBox()
        msg_box.setText("Data saved")
        msg_box.setWindowTitle("Save Confirmation")
        msg_box.exec_()

    #Called when user clicks save button next to description box
    def save_description(self, json_filepath, updated_information):
        set_project_info(json_filepath, 'project_description', updated_information)
        self.show_save_message()

    #Called when user wants to save any changes to the contributors
    def save_contributors(self, json_filepath):
        line_value = self.project_contributors.text()
        set_project_info(json_filepath, 'project_contributors', line_value)
        self.show_save_message()