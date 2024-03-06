"""
Acceleration based condition inidicators.

Most of the indicators implemenations are based on the ones found in below paper.

Vikas Sharma, Anand Parey,
A Review of Gear Fault Diagnosis Using Various Condition Indicators,
Procedia Engineering,
Volume 144,
2016,
Pages 253-263,
ISSN 1877-7058,
https://doi.org/10.1016/j.proeng.2016.05.131.
(https://www.sciencedirect.com/science/article/pii/S1877705816303484)
"""

import numpy as np
from numpy import ndarray
from pandas import Series
from scipy.stats import kurtosis

from pdm_tools.main.scaler import scale


def peak_to_peak(data: ndarray | Series) -> ndarray:
    """Peak to peak.

    Equals to difference between maximum and minimum value of the signal.

    Args:
        data (ndarray | Series): input acceleration signal

    Returns:
        ndarray: calculated peak to peak value
    """
    return np.ptp(data)

def zero_to_peak(data: ndarray | Series) -> ndarray:
    """Zero to peak.

    Equals to maximum value of the signal.

    Args:
        data (ndarray | Series): input acceleration signal

    Returns:
        ndarray: calculated zero to peak value
    """
    return np.max(data)

def rms(data: ndarray | Series) -> ndarray:
    """Calculates root mean square value of acceleration signal.

    Reflects the vibration amplitude and energy of signal in the time domain.

    Formula:
        RMS = sqrt(sum(x^2)/N), where: N - length, x - data

    Args:
        data (ndarray | Series): input acceleration signal

    Raises:
        ValueError: RMS value equals zero.

    Returns:
        ndarray: calculated rms value
    """
    if len(data) == 0:
        raise ValueError("Empty input data.")
    return np.sqrt(np.divide(np.sum(np.square(data)), len(data)))

def crest_factor(data: ndarray | Series) -> ndarray:
    """Crest factor.

    Peak value divided by the RMS. Faults often first manifest themselves in changes in the peakiness of a signal
    before they manifest in the energy represented by the signal root mean squared.
    The crest factor can provide an early warning for faults when they first develop.

    Args:
        data (ndarray | Series): input acceleration signal

    Raises:
        ValueError: RMS value equals zero.

    Returns:
        ndarray: calculated crest factor
    """
    if rms(data) == 0:
        raise ValueError("RMS value equals zero.")
    return np.max(data) / rms(data)

def std(data: ndarray | Series) -> ndarray:
    """Standard deviation.

    Args:
        data (ndarray | Series): input acceleration signal

    Returns:
        ndarray: calculated standard deviation
    """
    return np.std(data)

def kurt(data: ndarray | Series) -> ndarray:
    """Kurtosis.

    Kurtosis is the fourth order normalized moment of a given signal and provides a measure of the
    peakedness of the signal. Developing faults can increase the number of outliers,
    and therefore increase the value of the kurtosis metric.

    Args:
        data (ndarray | Series): input acceleration signal

    Returns:
        ndarray: calculated curtosis
    """
    return kurtosis(data, fisher = False)

def shape_factor(data: ndarray | Series) -> ndarray:
    """Shape factor

    Used to to represent the time series distribution of the signal in the time domain.

    Args:
        data (ndarray | Series): input acceleration signal

    Returns:
        ndarray: calculated shape factor
    """
    return rms(data) / np.divide(np.sum(np.abs(data)), len(data))

def mean_freq(data: ndarray | Series, frequency: ndarray | Series) -> ndarray:
    """Mean frequency

    It is a frequency domain parameter, extracted from the frequency spectrum of the gear vibration signal.
    MF indicates the vibration energy in the frequency domain.

    Args:
        data (ndarray | Series): input acceleration signal
        frequency (ndarray | Series): input frequency signal

    Returns:
        ndarray: calculated mean frequency
    """
    return sum(np.multiply(data, frequency)) / sum(data)

def freq_center(data: ndarray | Series, frequency: ndarray | Series) -> ndarray:
    """Frequency center

    FC shows the position changes of the main frequencies.

    Args:
        data (ndarray | Series): input acceleration signal
        frequency (ndarray | Series): input frequency signal

    Returns:
        ndarray: calculated frequency center
    """
    return sum(np.multiply(frequency, np.multiply(data, frequency))) / sum(np.multiply(data, frequency))

def vrms(data: ndarray | Series, fs: float, cutoff_start: float, cutoff_stop: float) -> ndarray:
    """FC shows the position changes of the main frequencies.

    Args:
        data (ndarray | Series): input acceleration signal
        fs (float): input signal's sampling frequency
        cutoff_start (float): bandpass cutoff start frequency
        cutoff_stop (float): bandpass cutoff stop frequency

    Returns:
        ndarray: calculated VRMS

    Scale extracted Acceleration components to Velocity (omega arithmetics)"""
    vel = np.multiply(np.divide(1, 2*np.pi*data), np.cos(2*np.pi*data))

    #Scale velocity to mm/s
    vel = scale(vel)

    #Spectral resolution
    df = fs/len(data)
    #Calculate index corresponding to cutoff frequency
    i_start = cutoff_start//df
    i_stop = cutoff_stop//df

    #Selected bandpass components
    vel = vel[int(i_start):int(i_stop)]

    #RMS of filtered velocity signal, from Parseval's Theorem
    return np.divide(np.sqrt(np.sum(np.square(data))), len(data))

