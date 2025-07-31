import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget,
    QTextEdit, QLineEdit, QMessageBox, QFormLayout, QFileDialog, QCheckBox, QComboBox
)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure


# Custom widget for the data page
class DataPageWidget(QWidget):
    uploadRequested = pyqtSignal()
    livestreamRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        self.upload_button = QPushButton("+ Upload EEG Data (.edf files only)")
        self.livestream_button = QPushButton("Livestream EEG Data")
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.livestream_button)
        layout.addLayout(button_layout)

        # Preview canvas using matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Metadata label
        self.metadata_label = QLabel("No data loaded")
        layout.addWidget(self.metadata_label)

        self.setLayout(layout)

        # Connect buttons to signals
        self.upload_button.clicked.connect(self.uploadRequested)
        self.livestream_button.clicked.connect(self.livestreamRequested)

    #Data Page Functions
    def on_upload_eeg(self):
        # Open file dialog to select .edf files
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload EEG Data", "", "EDF files (*.edf)")
        if file_name:
            # Placeholder: Update preview with a simple plot and metadata
            ax = self.data_page.figure.add_subplot(111)
            ax.clear()
            ax.plot([0, 1, 2], [0, 1, 0])  # Replace this with actual EEG data later
            self.data_page.canvas.draw()
            self.data_page.metadata_label.setText(f"File: {file_name}")

    def on_livestream_eeg(self):
        # Placeholder for livestream functionality
        self.metadata_label.setText("Livestreaming EEG Data...")

        