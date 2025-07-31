from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QCheckBox, QComboBox, QScrollArea, QGroupBox, QListWidget,
    QListWidgetItem
)

from PyQt5.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class PreprocessingPageWidget(QWidget):
    preprocessRequested = pyqtSignal(list)  # Signal now emits a list of transformation dictionaries

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Filtering section
        filter_group = QGroupBox("Filtering Options")
        filter_layout = QVBoxLayout()
        filter_label = QLabel("Select filters to apply:")
        filter_layout.addWidget(filter_label)

        # High-pass filter
        self.highpass_cb = QCheckBox("Enable High-pass Filter")
        self.highpass_input = QLineEdit("0.1")
        highpass_hbox = QHBoxLayout()
        highpass_hbox.addWidget(self.highpass_cb)
        highpass_hbox.addWidget(QLabel("Cutoff (Hz):"))
        highpass_hbox.addWidget(self.highpass_input)
        filter_layout.addLayout(highpass_hbox)

        # Band-pass filter
        self.bandpass_cb = QCheckBox("Enable Band-pass Filter")
        self.bandpass_low = QLineEdit("8")
        self.bandpass_high = QLineEdit("30")
        bandpass_hbox = QHBoxLayout()
        bandpass_hbox.addWidget(self.bandpass_cb)
        bandpass_hbox.addWidget(QLabel("Low (Hz):"))
        bandpass_hbox.addWidget(self.bandpass_low)
        bandpass_hbox.addWidget(QLabel("High (Hz):"))
        bandpass_hbox.addWidget(self.bandpass_high)
        filter_layout.addLayout(bandpass_hbox)

        # Notch filter
        self.notch_cb = QCheckBox("Enable Notch Filter")
        self.notch_freq = QComboBox()
        self.notch_freq.addItems(["50 Hz", "60 Hz"])
        notch_hbox = QHBoxLayout()
        notch_hbox.addWidget(self.notch_cb)
        notch_hbox.addWidget(QLabel("Frequency:"))
        notch_hbox.addWidget(self.notch_freq)
        filter_layout.addLayout(notch_hbox)

        apply_filter_button = QPushButton("Add Filters to Pipeline")
        apply_filter_button.clicked.connect(self.apply_filters)
        filter_layout.addWidget(apply_filter_button)
        filter_group.setLayout(filter_layout)
        scroll_layout.addWidget(filter_group)

        # Artifact Removal section
        artifact_group = QGroupBox("Artifact Removal")
        artifact_layout = QVBoxLayout()
        artifact_label = QLabel("Select artifact removal methods:")
        artifact_layout.addWidget(artifact_label)

        # ICA
        self.ica_cb = QCheckBox("Enable ICA")
        self.ica_button = QPushButton("Run ICA and Show Components")
        self.ica_button.clicked.connect(self.run_ica)
        ica_hbox = QHBoxLayout()
        ica_hbox.addWidget(self.ica_cb)
        ica_hbox.addWidget(self.ica_button)
        artifact_layout.addLayout(ica_hbox)

        # ASR
        self.asr_cb = QCheckBox("Enable ASR")
        self.asr_threshold = QLineEdit("20")
        self.asr_remove = QCheckBox("Remove Bad Data (vs. Correct)")
        asr_hbox = QHBoxLayout()
        asr_hbox.addWidget(self.asr_cb)
        asr_hbox.addWidget(QLabel("Std Dev Cutoff:"))
        asr_hbox.addWidget(self.asr_threshold)
        asr_hbox.addWidget(self.asr_remove)
        artifact_layout.addLayout(asr_hbox)

        apply_artifact_button = QPushButton("Add Artifact Removal to Pipeline")
        apply_artifact_button.clicked.connect(self.apply_artifact_removal)
        artifact_layout.addWidget(apply_artifact_button)
        artifact_group.setLayout(artifact_layout)
        scroll_layout.addWidget(artifact_group)

        # Signal Enhancement section
        enhancement_group = QGroupBox("Signal Enhancement")
        enhancement_layout = QVBoxLayout()
        enhancement_label = QLabel("Select signal enhancement methods:")
        enhancement_layout.addWidget(enhancement_label)

        # Re-referencing
        self.reref_cb = QCheckBox("Enable Re-referencing")
        self.reref_type = QComboBox()
        self.reref_type.addItems(["Common Average", "Cz", "Mastoid"])
        reref_hbox = QHBoxLayout()
        reref_hbox.addWidget(self.reref_cb)
        reref_hbox.addWidget(QLabel("Reference:"))
        reref_hbox.addWidget(self.reref_type)
        enhancement_layout.addLayout(reref_hbox)

        # Resampling
        self.resample_cb = QCheckBox("Enable Resampling")
        self.resample_rate = QLineEdit("256")
        resample_hbox = QHBoxLayout()
        resample_hbox.addWidget(self.resample_cb)
        resample_hbox.addWidget(QLabel("Sampling Rate (Hz):"))
        resample_hbox.addWidget(self.resample_rate)
        enhancement_layout.addLayout(resample_hbox)

        apply_enhancement_button = QPushButton("Add Signal Enhancement to Pipeline")
        apply_enhancement_button.clicked.connect(self.apply_signal_enhancement)
        enhancement_layout.addWidget(apply_enhancement_button)
        enhancement_group.setLayout(enhancement_layout)
        scroll_layout.addWidget(enhancement_group)

        # Status label
        self.status_label = QLabel("No preprocessing applied")
        scroll_layout.addWidget(self.status_label)

        # Selected Transformations section (as per your comment)
        transform_group = QGroupBox("Preprocessing Pipeline")
        transform_layout = QVBoxLayout()
        transform_label = QLabel("Selected Transformations (drag to reorder):")
        transform_layout.addWidget(transform_label)
        self.transform_list = QListWidget()
        self.transform_list.setDragDropMode(QListWidget.InternalMove)
        transform_layout.addWidget(self.transform_list)
        
        #Apply Changes Button
        apply_all_button = QPushButton("Apply All Changes")
        apply_all_button.clicked.connect(self.apply_all_changes)

        transform_layout.addWidget(apply_all_button)
        transform_group.setLayout(transform_layout)
        scroll_layout.addWidget(transform_group)

        # Raw Data Preview
        raw_data_label = QLabel("Raw EEG Data:")
        scroll_layout.addWidget(raw_data_label)
        self.raw_data_figure = Figure()
        self.raw_data_canvas = FigureCanvas(self.raw_data_figure)
        self.raw_data_canvas.setMinimumHeight(400)  # Custom height
        scroll_layout.addWidget(self.raw_data_canvas)

        # Processed Data Preview
        processed_data_label = QLabel("Processed EEG Data:")
        scroll_layout.addWidget(processed_data_label)
        self.processed_data_figure = Figure()
        self.processed_data_canvas = FigureCanvas(self.processed_data_figure)
        self.processed_data_canvas.setMinimumHeight(400)  # Custom height
        scroll_layout.addWidget(self.processed_data_canvas)

        # Set up scroll area
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)    #Makes me able to scroll vertically
        main_layout.addWidget(scroll_area)

    def apply_filters(self):
        """Add selected filters to the transformation list."""
        if self.highpass_cb.isChecked():
            cutoff = self.highpass_input.text()
            item = QListWidgetItem(f"High-pass Filter: {cutoff} Hz")
            item.setData(Qt.UserRole, {"type": "highpass", "params": {"cutoff": float(cutoff)}})
            self.transform_list.addItem(item)
        if self.bandpass_cb.isChecked():
            low = self.bandpass_low.text()
            high = self.bandpass_high.text()
            item = QListWidgetItem(f"Band-pass Filter: {low}-{high} Hz")
            item.setData(Qt.UserRole, {"type": "bandpass", "params": {"low": float(low), "high": float(high)}})
            self.transform_list.addItem(item)
        if self.notch_cb.isChecked():
            freq = self.notch_freq.currentText().split()[0]
            item = QListWidgetItem(f"Notch Filter: {freq} Hz")
            item.setData(Qt.UserRole, {"type": "notch", "params": {"freq": float(freq)}})
            self.transform_list.addItem(item)
        self.status_label.setText("Filters added to pipeline")

    def run_ica(self):
        """Run ICA and show components (kept separate for now)."""
        self.preprocessRequested.emit([{"type": "ica", "params": {}}])
        self.status_label.setText("ICA components computed")

    def apply_artifact_removal(self):
        """Add selected artifact removal methods to the transformation list."""
        if self.ica_cb.isChecked():
            item = QListWidgetItem("ICA")
            item.setData(Qt.UserRole, {"type": "ica", "params": {}})
            self.transform_list.addItem(item)
        if self.asr_cb.isChecked():
            threshold = self.asr_threshold.text()
            remove = self.asr_remove.isChecked()
            item = QListWidgetItem(f"ASR: threshold={threshold}, remove={remove}")
            item.setData(Qt.UserRole, {"type": "asr", "params": {"threshold": float(threshold), "remove": remove}})
            self.transform_list.addItem(item)
        self.status_label.setText("Artifact removal methods added to pipeline")

    def apply_signal_enhancement(self):
        """Add selected signal enhancement methods to the transformation list."""
        if self.reref_cb.isChecked():
            ref_type = self.reref_type.currentText()
            item = QListWidgetItem(f"Re-reference: {ref_type}")
            item.setData(Qt.UserRole, {"type": "reref", "params": {"ref_type": ref_type}})
            self.transform_list.addItem(item)
        if self.resample_cb.isChecked():
            rate = self.resample_rate.text()
            item = QListWidgetItem(f"Resample: {rate} Hz")
            item.setData(Qt.UserRole, {"type": "resample", "params": {"rate": float(rate)}})
            self.transform_list.addItem(item)
        self.status_label.setText("Signal enhancement methods added to pipeline")

    def apply_all_changes(self):
        """Emit the list of selected transformations in the specified order."""
        transformations = []
        for i in range(self.transform_list.count()):
            item = self.transform_list.item(i)
            transformation = item.data(Qt.UserRole)
            transformations.append(transformation)
        self.preprocessRequested.emit(transformations)
        self.status_label.setText("All changes applied")

    #Pre-processing Page Functions
    def on_preprocess(self, action, params):
            # Placeholder for preprocessing logic
            # Integrate with mne for actual processing
        if action == "filter":
            if params["highpass"]:
                    # Example: raw.filter(l_freq=params["highpass"], h_freq=None)
                pass
            if params["bandpass_low"] and params["bandpass_high"]:
                    # Example: raw.filter(l_freq=params["bandpass_low"], h_freq=params["bandpass_high"])
                pass
            if params["notch"]:
                    # Example: raw.notch_filter(freqs=[params["notch"]])
                pass
        elif action == "ica":
                # Example: ica = mne.preprocessing.ICA().fit(raw)
            pass
        elif action == "artifact_removal":
                # Example: Implement ASR using mne.preprocessing
            pass
        elif action == "signal_enhancement":
            if params["reref_type"]:
                    # Example: raw.set_eeg_reference(params["reref_type"])
                pass
            if params["resample_rate"]:
                    # Example: raw.resample(params["resample_rate"])
                pass
        ### Create conditional for when the action is to apply transformations