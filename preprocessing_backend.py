import mne
import os

def process_edf_file(filepath, transformation_func):
    """
    Helper function to read an EDF file, apply a transformation, and overwrite the file.
    
    Parameters:
    filepath (str): Path to the EDF file.
    transformation_func (function): Function that takes a Raw object and returns a transformed Raw object.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} not found")
    raw = mne.io.read_raw_edf(filepath, preload=True)
    transformed_raw = transformation_func(raw)
    mne.export.export_raw(filepath, transformed_raw, fmt='edf', overwrite=True)

def high_pass_filter(filepath, cutoff):
    """
    Apply a high-pass filter to the EEG data.
    
    Parameters:
    filepath (str): Path to the EDF file.
    cutoff (float): Cutoff frequency for the high-pass filter in Hz.
    """
    def transformation(raw):
        raw.filter(l_freq=cutoff, h_freq=None)
        return raw
    process_edf_file(filepath, transformation)

def band_pass_filter(filepath, low_freq, high_freq):
    """
    Apply a band-pass filter to the EEG data.
    
    Parameters:
    filepath (str): Path to the EDF file.
    low_freq (float): Lower frequency for the band-pass filter in Hz.
    high_freq (float): Upper frequency for the band-pass filter in Hz.
    """
    def transformation(raw):
        raw.filter(l_freq=low_freq, h_freq=high_freq)
        return raw
    process_edf_file(filepath, transformation)

def low_pass_filter(filepath, cutoff):
    """
    Apply a low-pass filter to the EEG data.
    
    Parameters:
    filepath (str): Path to the EDF file.
    cutoff (float): Cutoff frequency for the low-pass filter in Hz.
    """
    def transformation(raw):
        raw.filter(l_freq=None, h_freq=cutoff)
        return raw
    process_edf_file(filepath, transformation)

def notch_filter(filepath, freq):
    """
    Apply a notch filter to the EEG data to remove specific frequency noise.
    
    Parameters:
    filepath (str): Path to the EDF file.
    freq (float): Frequency to be notched in Hz (e.g., 50 or 60 for power line noise).
    """
    def transformation(raw):
        raw.notch_filter(freqs=[freq])
        return raw
    process_edf_file(filepath, transformation)

def ica(filepath):
    """
    Apply Independent Component Analysis (ICA) to remove artifacts from the EEG data.
    
    Parameters:
    filepath (str): Path to the EDF file.
    """
    def transformation(raw):
        ica = mne.preprocessing.ICA(n_components=15, random_state=97)
        ica.fit(raw)
        eog_indices, _ = ica.find_bads_eog(raw)
        ica.exclude = eog_indices
        ica.apply(raw)
        return raw
    process_edf_file(filepath, transformation)

def asr(filepath, std_cutoff, remove_or_correct):
    """
    Apply Artifact Subspace Reconstruction (ASR) to the EEG data.
    
    Parameters:
    filepath (str): Path to the EDF file.
    std_cutoff (float): Standard deviation cutoff for artifact detection.
    remove_or_correct (bool): Whether to remove (True) or correct (False) artifacts.
    
    Note: This is a placeholder. Implement ASR using an appropriate library or method.
    """
    def transformation(raw):
        # Placeholder: Implement ASR using ASRpy
        # Example: cleaned_raw = asr_process(raw, std_cutoff, remove_or_correct)
        # For now, returns raw data unchanged
        return raw
    process_edf_file(filepath, transformation)

def rereference(filepath, reference):
    """
    Re-reference the EEG data to a specified reference.
    
    Parameters:
    filepath (str): Path to the EDF file.
    reference (str or list): Reference to use ('average' or list of channel names).
    """
    def transformation(raw):
        if reference == 'average':
            raw.set_eeg_reference('average')
        else:
            raw.set_eeg_reference(ref_channels=[reference])
        return raw
    process_edf_file(filepath, transformation)

def resample(filepath, sampling_rate):
    """
    Resample the EEG data to a new sampling rate.
    
    Parameters:
    filepath (str): Path to the EDF file.
    sampling_rate (float): New sampling rate in Hz.
    """
    def transformation(raw):
        raw.resample(sfreq=sampling_rate)
        return raw
    process_edf_file(filepath, transformation)