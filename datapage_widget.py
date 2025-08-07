from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QListWidget
)
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

# Custom widget for the data page
class DataPageWidget(QWidget):
    uploadRequested = pyqtSignal(list)  # Signal for concatenated file list
    livestreamRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Horizontal layout for upload and livestream options
        button_layout = QHBoxLayout()
        self.upload_button = QPushButton("+ Upload EEG Data (.edf files only)")
        self.livestream_button = QPushButton("Livestream EEG Data (LSL)")
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.livestream_button)
        layout.addLayout(button_layout)

        # List to show selected files
        self.data_list = QListWidget()
        self.data_list.setSelectionMode(QListWidget.MultiSelection)  # Allow multiple selections
        layout.addWidget(QLabel("Selected EEG Files:"))
        layout.addWidget(self.data_list)

        # Confirm and concatenate button
        self.confirm_button = QPushButton("Confirm Selected Data")
        self.confirm_button.clicked.connect(self.confirm_and_concatenate)
        layout.addWidget(self.confirm_button)

        # Preview canvas using matplotlib
        self.preview_label = QLabel("Preview Selected Data:")
        layout.addWidget(self.preview_label)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Metadata label
        self.metadata_label = QLabel("No data loaded")
        layout.addWidget(self.metadata_label)

        self.setLayout(layout)

        # Connect buttons to signals
        self.upload_button.clicked.connect(self.on_upload_eeg)
        self.livestream_button.clicked.connect(self.livestreamRequested)

    def on_upload_eeg(self):
        """Add selected .edf files to the list widget."""
        file_names, _ = QFileDialog.getOpenFileNames(self, "Upload EEG Data", "", "EDF files (*.edf)")
        for file_name in file_names:
            if file_name and file_name not in [self.data_list.item(i).text() for i in range(self.data_list.count())]:
                self.data_list.addItem(file_name)
        self.metadata_label.setText(f"{self.data_list.count()} file(s) selected")

    def confirm_and_concatenate(self):
        """Emit signal with list of selected files and update preview."""
        file_list = [self.data_list.item(i).text() for i in range(self.data_list.count())]
        if file_list:
            self.uploadRequested.emit(file_list)
            # Placeholder: Update preview with a simple plot
            ax = self.figure.add_subplot(111)
            ax.clear()
            ax.plot([0, 1, 2], [0, 1, 0])  # Replace with actual EEG data later
            self.canvas.draw()
            self.metadata_label.setText(f"Concatenated {len(file_list)} file(s)")
        else:
            self.metadata_label.setText("No files selected")

    def on_livestream_eeg(self):
        """Placeholder for livestream functionality."""
        self.metadata_label.setText("Livestreaming EEG Data...")