from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QCheckBox, QComboBox, QScrollArea, QGroupBox, QListWidget,
    QListWidgetItem, QRadioButton, QButtonGroup
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

        # Offering the mainly used types of filters
        self.signal_filter_label = QLabel("Select specific filtering method:")
        filter_layout.addWidget(self.signal_filter_label)

        self.filter_button_group = QButtonGroup()
        self.butterworth_option = QRadioButton("Butterworth")
        self.chebyshev_one_option = QRadioButton("Chebyshev I")
        self.chebyshev_two_option = QRadioButton("Chebyshev II")
        self.bessel_option = QRadioButton("Bessel")
        self.fir_option = QRadioButton("Finite Impulse Response")
        self.none_option = QRadioButton("None")

        self.filter_button_group.addButton(self.butterworth_option)
        self.filter_button_group.addButton(self.chebyshev_one_option)
        self.filter_button_group.addButton(self.chebyshev_two_option)
        self.filter_button_group.addButton(self.bessel_option)
        self.filter_button_group.addButton(self.fir_option)
        self.filter_button_group.addButton(self.none_option)

        self.specific_filter_layout = QHBoxLayout()

        self.specific_filter_layout.addWidget(self.butterworth_option)
        self.specific_filter_layout.addWidget(self.chebyshev_one_option)
        self.specific_filter_layout.addWidget(self.chebyshev_two_option)
        self.specific_filter_layout.addWidget(self.bessel_option)
        self.specific_filter_layout.addWidget(self.fir_option)
        self.specific_filter_layout.addWidget(self.none_option)

        filter_layout.addLayout(self.specific_filter_layout)

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

        # Low-pass filter
        self.lowpass_cb = QCheckBox("Enable Low-pass Filter")
        self.lowpass_input = QLineEdit("0.1")
        lowpass_hbox = QHBoxLayout()
        lowpass_hbox.addWidget(self.lowpass_cb)
        lowpass_hbox.addWidget(QLabel("Cutoff (Hz):"))
        lowpass_hbox.addWidget(self.lowpass_input)
        filter_layout.addLayout(lowpass_hbox)

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

        # Adjust Roll-off for filters
        self.roll_off = QCheckBox("Manually set roll-off/slope (db/octave)")
        self.roll_off_input = QLineEdit("20")
        rolloff_hbox = QHBoxLayout()
        rolloff_hbox.addWidget(self.roll_off)
        rolloff_hbox.addWidget(QLabel("Slope (db/octave):"))
        rolloff_hbox.addWidget(self.roll_off_input)
        filter_layout.addLayout(rolloff_hbox)

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

        # Selected Transformations section
        transform_group = QGroupBox("Preprocessing Pipeline")
        transform_layout = QVBoxLayout()
        transform_label = QLabel("Selected Transformations (drag to reorder):")
        transform_layout.addWidget(transform_label)

        # List Options
        self.transform_list = QListWidget()
        self.transform_list.setDragDropMode(QListWidget.InternalMove)
        transform_layout.addWidget(self.transform_list)
        
        # Apply Changes Button
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
        self.raw_data_canvas.setMinimumHeight(400)
        scroll_layout.addWidget(self.raw_data_canvas)

        # Processed Data Preview
        processed_data_label = QLabel("Processed EEG Data:")
        scroll_layout.addWidget(processed_data_label)
        self.processed_data_figure = Figure()
        self.processed_data_canvas = FigureCanvas(self.processed_data_figure)
        self.processed_data_canvas.setMinimumHeight(400)
        scroll_layout.addWidget(self.processed_data_canvas)

        # Set up scroll area
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

    def apply_filters(self):
        """Add selected filters with their implementation type and roll-off to the transformation list."""
        # Get the selected filter type
        selected_filter = self.filter_button_group.checkedButton()
        filter_type = selected_filter.text() if selected_filter else "None"

        # Get roll-off if enabled
        roll_off = None
        if self.roll_off.isChecked():
            try:
                roll_off = float(self.roll_off_input.text())
            except ValueError:
                self.status_label.setText("Error: Invalid roll-off value")
                return

        # Define implementation parameters based on filter type
        if filter_type == "Butterworth":
            impl_params = {"method": "iir", "iir_params": {"ftype": "butter", "order": 4}}
        elif filter_type == "Chebyshev I":
            impl_params = {"method": "iir", "iir_params": {"ftype": "cheby1", "order": 4, "rp": 0.5}}
        elif filter_type == "Chebyshev II":
            impl_params = {"method": "iir", "iir_params": {"ftype": "cheby2", "order": 4, "rs": 40}}
        elif filter_type == "Bessel":
            impl_params = {"method": "iir", "iir_params": {"ftype": "bessel", "order": 4}}
        elif filter_type == "Finite Impulse Response":
            impl_params = {"method": "fir", "fir_window": "hamming"}
        else:
            impl_params = {"method": "iir", "iir_params": {"ftype": "butter", "order": 4}}  # Default
            self.status_label.setText("No filter type selected; using default (Butterworth)")

        # Add enabled filters to the pipeline
        if self.highpass_cb.isChecked():
            try:
                cutoff = float(self.highpass_input.text())
                params = {"l_freq": cutoff, "h_freq": None, **impl_params}
                if roll_off is not None:
                    params["roll_off"] = roll_off
                item_text = f"High-pass Filter ({filter_type}): {cutoff} Hz"
                if roll_off is not None:
                    item_text += f", Roll-off: {roll_off} dB/oct"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, {"type": "filter", "params": params})
                self.transform_list.addItem(item)
            except ValueError:
                self.status_label.setText("Error: Invalid high-pass cutoff")
                return

        if self.lowpass_cb.isChecked():
            try:
                cutoff = float(self.lowpass_input.text())
                params = {"l_freq": None, "h_freq": cutoff, **impl_params}
                if roll_off is not None:
                    params["roll_off"] = roll_off
                item_text = f"Low-pass Filter ({filter_type}): {cutoff} Hz"
                if roll_off is not None:
                    item_text += f", Roll-off: {roll_off} dB/oct"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, {"type": "filter", "params": params})
                self.transform_list.addItem(item)
            except ValueError:
                self.status_label.setText("Error: Invalid low-pass cutoff")
                return

        if self.bandpass_cb.isChecked():
            try:
                low = float(self.bandpass_low.text())
                high = float(self.bandpass_high.text())
                params = {"l_freq": low, "h_freq": high, **impl_params}
                if roll_off is not None:
                    params["roll_off"] = roll_off
                item_text = f"Band-pass Filter ({filter_type}): {low}-{high} Hz"
                if roll_off is not None:
                    item_text += f", Roll-off: {roll_off} dB/oct"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, {"type": "filter", "params": params})
                self.transform_list.addItem(item)
            except ValueError:
                self.status_label.setText("Error: Invalid band-pass frequencies")
                return

        if self.notch_cb.isChecked():
            try:
                freq = float(self.notch_freq.currentText().split()[0])
                params = {"freqs": [freq], **impl_params}
                if roll_off is not None:
                    params["roll_off"] = roll_off
                item_text = f"Notch Filter ({filter_type}): {freq} Hz"
                if roll_off is not None:
                    item_text += f", Roll-off: {roll_off} dB/oct"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, {"type": "notch", "params": params})
                self.transform_list.addItem(item)
            except ValueError:
                self.status_label.setText("Error: Invalid notch frequency")
                return

        self.status_label.setText("Filters added to pipeline")

    def run_ica(self):
        """Run ICA and show components (kept separate for now)."""
        self.preprocessRequested.emit([{"type": "ica", "params": {}}])
        self.status_label.setText("ICA components computed")

    def apply_artifact_removal(self):
        """Add selected artifact removal methods to the transformation list."""
        try:
            if self.ica_cb.isChecked():
                item = QListWidgetItem("ICA")
                item.setData(Qt.UserRole, {"type": "ica", "params": {}})
                self.transform_list.addItem(item)
            if self.asr_cb.isChecked():
                threshold = float(self.asr_threshold.text())
                remove = self.asr_remove.isChecked()
                item = QListWidgetItem(f"ASR: threshold={threshold}, remove={remove}")
                item.setData(Qt.UserRole, {"type": "asr", "params": {"threshold": threshold, "remove": remove}})
                self.transform_list.addItem(item)
            self.status_label.setText("Artifact removal methods added to pipeline")
        except ValueError:
            self.status_label.setText("Error: Invalid ASR threshold")

    def apply_signal_enhancement(self):
        """Add selected signal enhancement methods to the transformation list."""
        try:
            if self.reref_cb.isChecked():
                ref_type = self.reref_type.currentText()
                item = QListWidgetItem(f"Re-reference: {ref_type}")
                item.setData(Qt.UserRole, {"type": "reref", "params": {"ref_type": ref_type}})
                self.transform_list.addItem(item)
            if self.resample_cb.isChecked():
                rate = float(self.resample_rate.text())
                item = QListWidgetItem(f"Resample: {rate} Hz")
                item.setData(Qt.UserRole, {"type": "resample", "params": {"rate": rate}})
                self.transform_list.addItem(item)
            self.status_label.setText("Signal enhancement methods added to pipeline")
        except ValueError:
            self.status_label.setText("Error: Invalid resampling rate")

    #This function just transfers data from self.transformation_list to an empty list
    def apply_all_changes(self):
        """Emit the list of selected transformations in the specified order."""
        transformations = []
        for i in range(self.transform_list.count()):
            item = self.transform_list.item(i)
            transformation = item.data(Qt.UserRole)
            transformations.append(transformation)
        self.preprocessRequested.emit(transformations)
        self.status_label.setText("All changes applied")

    #This will be responsible for calling the correct backend functions (based on dictionary specifications)
    def on_preprocess(self, action, params):
        """Placeholder for preprocessing logic, integrating with MNE."""
        try:
            if action == "filter":
                # Calculate order based on roll-off if provided
                if "roll_off" in params:
                    # Example: Adjust order based on roll-off (simplified)
                    # For IIR filters, roll-off is ~6 dB/octave per order
                    order = params.get("iir_params", {}).get("order", 4)
                    if params["roll_off"] > 0:
                        order = max(1, int(params["roll_off"] / 6))  # Approximate
                        params["iir_params"]["order"] = order
                    elif params["method"] == "fir":
                        # For FIR, roll-off affects window length (simplified)
                        params["fir_length"] = max(101, int(params["roll_off"] * 10))  # Example scaling
                # Example: raw.filter(l_freq=params["l_freq"], h_freq=params["h_freq"], 
                #                     method=params["method"], iir_params=params.get("iir_params"), 
                #                     fir_window=params.get("fir_window"), fir_length=params.get("fir_length"))
                pass
            elif action == "notch":
                if "roll_off" in params:
                    # Similar adjustment for notch filter
                    order = params.get("iir_params", {}).get("order", 4)
                    if params["roll_off"] > 0:
                        order = max(1, int(params["roll_off"] / 6))
                        params["iir_params"]["order"] = order
                    elif params["method"] == "fir":
                        params["fir_length"] = max(101, int(params["roll_off"] * 10))
                # Example: raw.notch_filter(freqs=params["freqs"], method=params["method"], 
                #                           iir_params=params.get("iir_params"), 
                #                           fir_window=params.get("fir_window"), fir_length=params.get("fir_length"))
                pass
            elif action == "ica":
                # Example: ica = mne.preprocessing.ICA().fit(raw)
                pass
            elif action == "asr":
                # Example: Implement ASR using mne.preprocessing
                pass
            elif action == "reref":
                # Example: raw.set_eeg_reference(params["ref_type"])
                pass
            elif action == "resample":
                # Example: raw.resample(params["rate"])
                pass
        except Exception as e:
            self.status_label.setText(f"Error in preprocessing: {str(e)}")