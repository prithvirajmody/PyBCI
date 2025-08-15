from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit,
    QGroupBox, QTabWidget, QFileDialog, QScrollArea
)
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import pyqtgraph.opengl as gl   #Added for 3D rendering

class VisualizationPageWidget(QWidget):
    plotRequested = pyqtSignal(str, dict)  # Signal for plot requests (type, parameters)

    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Status label
        self.status_label = QLabel("No data loaded")
        scroll_layout.addWidget(self.status_label)

        # Tabbed layout for visualization types
        self.vis_tabs = QTabWidget()
        self.vis_tabs.addTab(self.create_eeg_tab(), "EEG Data")
        self.vis_tabs.addTab(self.create_model_tab(), "Model Evaluation")
        self.vis_tabs.addTab(self.create_real_time_tab(), "Real-Time")
        scroll_layout.addWidget(self.vis_tabs)

        # Export button
        export_button = QPushButton("Export Visualization")
        export_button.clicked.connect(self.export_plot)
        scroll_layout.addWidget(export_button)

        # Set up scroll area
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

    def create_eeg_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Channel selection
        channel_group = QGroupBox("Channel Selection")
        channel_layout = QHBoxLayout()
        channel_label = QLabel("Select Channels:")
        self.channel_combo = QComboBox()
        channel_layout.addWidget(channel_label)
        channel_layout.addWidget(self.channel_combo)
        channel_group.setLayout(channel_layout)
        layout.addWidget(channel_group)

        # Plot type selection
        plot_type_group = QGroupBox("Plot Type")
        plot_type_layout = QHBoxLayout()
        plot_type_label = QLabel("Select Plot Type:")
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(["Time-Series", "Topographic Map", "Spectrogram", "ERP"])
        plot_type_layout.addWidget(plot_type_label)
        plot_type_layout.addWidget(self.plot_type_combo)
        plot_type_group.setLayout(plot_type_layout)
        layout.addWidget(plot_type_group)

        # Time window selection
        time_group = QGroupBox("Time Window")
        time_layout = QHBoxLayout()
        self.time_start = QLineEdit("0")
        self.time_end = QLineEdit("10")
        time_layout.addWidget(QLabel("Start Time (s):"))
        time_layout.addWidget(self.time_start)
        time_layout.addWidget(QLabel("End Time (s):"))
        time_layout.addWidget(self.time_end)
        time_group.setLayout(time_layout)
        layout.addWidget(time_group)

        # Frequency band selection
        freq_group = QGroupBox("Frequency Band")
        freq_layout = QHBoxLayout()
        self.freq_low = QLineEdit("8")
        self.freq_high = QLineEdit("30")
        freq_layout.addWidget(QLabel("Low Freq (Hz):"))
        freq_layout.addWidget(self.freq_low)
        freq_layout.addWidget(QLabel("High Freq (Hz):"))
        freq_layout.addWidget(self.freq_high)
        freq_group.setLayout(freq_layout)
        layout.addWidget(freq_group)

        # Plot canvas
        self.eeg_figure = Figure()
        self.eeg_canvas = FigureCanvas(self.eeg_figure)
        self.eeg_canvas.setMinimumHeight(400)
        layout.addWidget(self.eeg_canvas)

        # Update plot button
        update_button = QPushButton("Update EEG Plot")
        update_button.clicked.connect(self.update_eeg_plot)
        layout.addWidget(update_button)

        widget.setLayout(layout)
        return widget

    def create_model_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Model selection
        model_group = QGroupBox("Model Selection")
        model_layout = QHBoxLayout()
        model_label = QLabel("Select Model:")
        self.model_combo = QComboBox()
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)

        # Visualization type
        vis_type_group = QGroupBox("Visualization Type")
        vis_type_layout = QHBoxLayout()
        vis_type_label = QLabel("Select Visualization:")
        self.vis_type_combo = QComboBox()
        self.vis_type_combo.addItems(["Confusion Matrix", "ROC Curve", "Feature Importance", "Learning Curve"])
        vis_type_layout.addWidget(vis_type_label)
        vis_type_layout.addWidget(self.vis_type_combo)
        vis_type_group.setLayout(vis_type_layout)
        layout.addWidget(vis_type_group)

        # Plot canvas
        self.model_figure = Figure()
        self.model_canvas = FigureCanvas(self.model_figure)
        self.model_canvas.setMinimumHeight(400)
        layout.addWidget(self.model_canvas)

        # Update plot button
        update_button = QPushButton("Update Model Plot")
        update_button.clicked.connect(self.update_model_plot)
        layout.addWidget(update_button)

        widget.setLayout(layout)
        return widget

    def create_real_time_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # 3D Brain Model
        self.brain_view = gl.GLViewWidget()  # Create a 3D view widget
        self.brain_view.setCameraPosition(distance=200)  # Set initial camera distance
        layout.addWidget(self.brain_view)

        # Load a placeholder brain model (e.g., a sphere)
        # Replace this with an actual brain model (STL/OBJ) later
        brain_model = gl.GLMeshItem(
            meshdata=gl.MeshData.sphere(rows=10, cols=20),
            color=(0.5, 0.5, 0.5, 1)  # Gray color with full opacity
        )
        self.brain_view.addItem(brain_model)  # Add the model to the view
        self.brain_model = brain_model  # Store reference for updates

        # Real-time plot canvas (optional, keep if you still want 2D plots)
        self.real_time_figure = Figure()
        self.real_time_canvas = FigureCanvas(self.real_time_figure)
        self.real_time_canvas.setMinimumHeight(400)
        layout.addWidget(self.real_time_canvas)

        # Start/Stop streaming button
        self.stream_button = QPushButton("Start Streaming")
        self.stream_button.clicked.connect(self.toggle_streaming)
        layout.addWidget(self.stream_button)

        widget.setLayout(layout)
        return widget

    def update_eeg_plot(self):
        params = {
            "plot_type": self.plot_type_combo.currentText(),
            "channels": self.channel_combo.currentText(),
            "time_start": float(self.time_start.text()),
            "time_end": float(self.time_end.text()),
            "freq_low": float(self.freq_low.text()) if self.freq_low.text() else None,
            "freq_high": float(self.freq_high.text()) if self.freq_high.text() else None
        }
        self.plotRequested.emit("eeg", params)
        self.status_label.setText(f"Displaying {params['plot_type']}")

    def update_model_plot(self):
        params = {
            "vis_type": self.vis_type_combo.currentText(),
            "model": self.model_combo.currentText()
        }
        self.plotRequested.emit("model", params)
        self.status_label.setText(f"Displaying {params['vis_type']}")

    def toggle_streaming(self):
        self.plotRequested.emit("real_time", {})
        self.status_label.setText("Streaming started" if self.stream_button.text() == "Start Streaming" else "Streaming stopped")
        self.stream_button.setText("Stop Streaming" if self.stream_button.text() == "Start Streaming" else "Start Streaming")

    def export_plot(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Visualization", "", "PNG files (*.png);;PDF files (*.pdf)")
        if file_name:
            self.plotRequested.emit("export", {"file_name": file_name})
            self.status_label.setText(f"Plot saved to {file_name}")