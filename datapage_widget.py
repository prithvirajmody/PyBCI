from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QListWidget, QScrollArea, QComboBox
)
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import pyedflib
import numpy as np

#Import custom classes and functions
from Backend.data_backend import concatenate, store_new_input_file

class DataPageWidget(QWidget):
    uploadRequested = pyqtSignal(list)  # Signal for concatenated file list
    livestreamRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Scroll area to make the widget vertically scrollable
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Horizontal layout for upload and livestream options
        button_layout = QHBoxLayout()
        self.upload_button = QPushButton("+ Upload EEG Data (.edf files only)")
        self.livestream_button = QPushButton("Livestream EEG Data (LSL)")
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.livestream_button)
        scroll_layout.addLayout(button_layout)

        # List to show selected files
        self.data_list = QListWidget()
        self.data_list.setSelectionMode(QListWidget.MultiSelection)
        scroll_layout.addWidget(QLabel("Selected EEG Files:"))
        scroll_layout.addWidget(self.data_list)

        # Display mode selection
        display_layout = QHBoxLayout()
        display_label = QLabel("Display Mode:")
        self.display_combo = QComboBox()
        self.display_combo.addItems(["Separate Axes", "Same Axis"])
        display_layout.addWidget(display_label)
        display_layout.addWidget(self.display_combo)
        scroll_layout.addLayout(display_layout)

        # Confirm and concatenate button
        self.confirm_button = QPushButton("Confirm Selected Data")
        self.confirm_button.clicked.connect(self.confirm_and_concatenate)
        scroll_layout.addWidget(self.confirm_button)

        # Preview canvas
        self.preview_label = QLabel("Preview Selected Data:")
        scroll_layout.addWidget(self.preview_label)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(400)  # Ensure minimum visibility
        scroll_layout.addWidget(self.canvas)

        # Metadata label
        self.metadata_label = QLabel("No data loaded")
        scroll_layout.addWidget(self.metadata_label)

        # Add stretch to push content to top
        scroll_layout.addStretch()

        # Set up scroll area
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Connect buttons to signals
        self.upload_button.clicked.connect(self.on_upload_eeg)
        self.livestream_button.clicked.connect(self.livestreamRequested)

    def on_upload_eeg(self):
        """Add selected .edf files to the list widget."""
        file_names, _ = QFileDialog.getOpenFileNames(self, "Upload EEG Data", "", "EDF files (*.edf)")
        for file_name in file_names:
            if file_name and file_name not in [self.data_list.item(i).text() for i in range(self.data_list.count())]:
                self.data_list.addItem(file_name)
            #Upload files into input data directory
            store_new_input_file(file_name, 'abc')  #Use json.load to get project name
        self.metadata_label.setText(f"{self.data_list.count()} file(s) selected")

    def plot_edf_signals(self, filepath, display_choice='separate'):
        """
        Plot EEG signals from an EDF file on the widget's canvas.
        
        Parameters:
        filepath (str): Path to the EDF file.
        display_choice (str): 'same' for single axis with offsets, 'separate' for subplots.
        """
        try:
            f = pyedflib.EdfReader(filepath)
            n = f.signals_in_file
            signal_labels = f.getSignalLabels()
            sfreqs = [f.getSampleFrequency(i) for i in range(n)]
            sigbufs = [f.readSignal(i) for i in range(n)]
            f.close()
        except Exception as e:
            self.metadata_label.setText(f"Error loading EDF file: {str(e)}")
            return

        # Clear previous plot
        self.figure.clear()

        if display_choice == 'same':
            ax = self.figure.add_subplot(111)
            for i in range(n):
                time = np.arange(len(sigbufs[i])) / sfreqs[i]
                amplitude_range = np.ptp(sigbufs[i]) if len(sigbufs[i]) > 0 else 1
                offset = i * amplitude_range * 1.5
                ax.plot(time, sigbufs[i] + offset, label=signal_labels[i])
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude (uV)')
            ax.set_title('EEG Signal Waveform')
            ax.legend(loc='upper right')
            ax.grid(True)
        elif display_choice == 'separate':
            if n == 1:
                ax = self.figure.add_subplot(111)
                axs = [ax]
            else:
                axs = self.figure.subplots(nrows=n, ncols=1, sharex=True)
            for i in range(n):
                time = np.arange(len(sigbufs[i])) / sfreqs[i]
                axs[i].plot(time, sigbufs[i], label=signal_labels[i])
                axs[i].set_ylabel('Amplitude')
                axs[i].legend()
                axs[i].grid(True)
            axs[-1].set_xlabel('Time (s)')
            self.figure.suptitle('EDF Signal Waveform')

        self.figure.tight_layout()
        self.canvas.draw()

    def confirm_and_concatenate(self):
        """Emit signal with list of selected files and update preview."""
        file_list = [self.data_list.item(i).text() for i in range(self.data_list.count())]
        if file_list:
            self.uploadRequested.emit(file_list)
            # Plot the first selected file
            display_choice = 'separate' if self.display_combo.currentText() == "Separate Axes" else 'same'
            self.plot_edf_signals(file_list[0], display_choice=display_choice)
            self.metadata_label.setText(f"Concatenated {len(file_list)} file(s); previewing {file_list[0]}")
        else:
            self.metadata_label.setText("No files selected")
            self.figure.clear()
            self.canvas.draw()

    def on_livestream_eeg(self):
        """Placeholder for livestream functionality."""
        self.metadata_label.setText("Livestreaming EEG Data...")    