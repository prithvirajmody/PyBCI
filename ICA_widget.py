from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QCheckBox
)
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import mne
from mne.preprocessing import ICA

class IcaWidget(QWidget):
    icaComponentsSelected = pyqtSignal(list)  # Signal emitting indices of selected components

    def __init__(self, raw, num_channels, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Perform Independent Component Analysis")
        self.setMinimumSize(1000, 700)
        self.raw = raw  # Store MNE Raw object
        self.ica = None  # To store ICA object
        self.component_checkboxes = []  # Store checkboxes for components

        # Main layout with scroll area
        main_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)

        # Metadata label
        self.metadata_label = QLabel("No ICA performed")
        self.scroll_layout.addWidget(self.metadata_label)

        # Save components button
        self.save_button = QPushButton("Save Selected Components")
        self.save_button.clicked.connect(self.save_selected_components)
        self.scroll_layout.addWidget(self.save_button)

        # Add stretch to push content to top
        self.scroll_layout.addStretch()

        # Set up scroll area
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Automatically run ICA and plot
        self.run_ica_and_plot(num_channels)

    def run_ica_and_plot(self, num_channels):
        """Run ICA and display component plots with checkboxes on the left."""
        if self.raw is None:
            self.metadata_label.setText("No EEG data loaded")
            return

        try:
            # Determine number of components
            n_channels = len(self.raw.ch_names)
            n_components = min(num_channels, n_channels if num_channels > 20 else num_channels)

            # Run ICA
            self.ica = ICA(n_components=n_components, random_state=42)
            self.ica.fit(self.raw)
            self.metadata_label.setText(f"ICA computed with {n_components} components")

            # Clear previous plots and checkboxes
            self.component_checkboxes.clear()

            # Create a new figure for plots
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setMinimumHeight(200 * n_components)  # Dynamic height
            self.scroll_layout.insertWidget(0, self.canvas)  # Insert canvas at top

            # Plot components
            n_cols = 3  # Checkbox, time series, topography
            n_rows = n_components
            gs = self.figure.add_gridspec(n_rows, n_cols, width_ratios=[0.5, 3, 1])

            for i in range(n_components):
                # Create layout for checkbox and plots
                component_layout = QHBoxLayout()
                
                # Checkbox on the left
                checkbox = QCheckBox(f"IC {i}")
                checkbox.setChecked(True)  # Default: all components selected
                component_layout.addWidget(checkbox)
                self.component_checkboxes.append(checkbox)

                # Time series plot
                ax_time = self.figure.add_subplot(gs[i, 1])
                time = np.arange(min(1000, self.ica.n_samples_)) / self.raw.info['sfreq']  # Limit to 1000 samples
                ax_time.plot(time, self.ica.get_components()[:, i][:len(time)])
                ax_time.set_title(f"Component {i}")
                ax_time.set_ylabel("Amplitude")
                ax_time.grid(True)
                if i == n_components - 1:
                    ax_time.set_xlabel("Time (s)")

                # Topography plot
                ax_topo = self.figure.add_subplot(gs[i, 2])
                mne.viz.plot_ica_components(self.ica, picks=[i], axes=ax_topo, show=False)
                ax_topo.set_title("")

                # Add stretch to component layout
                component_layout.addStretch()
                self.scroll_layout.insertLayout(self.scroll_layout.count() - 2, component_layout)  # Before save button and stretch

            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as e:
            self.metadata_label.setText(f"Error running ICA: {str(e)}")

    def save_selected_components(self):
        """Emit selected component indices."""
        if self.ica is None:
            self.metadata_label.setText("No ICA performed")
            return

        selected_components = [i for i, checkbox in enumerate(self.component_checkboxes) if checkbox.isChecked()]
        self.icaComponentsSelected.emit(selected_components)
        self.metadata_label.setText(f"Selected {len(selected_components)} components")
        self.close()  # Close widget after saving