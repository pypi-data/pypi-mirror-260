"""Filter - stores all functions related to filtering."""

import pandas as pd
from numpy import ndarray
from scipy.signal import butter, sosfilt


class Butter:
    """Wrapper for scipy Butterworth filtering functionality."""
    def __init__(self,
                 lowcut: float | int | None = None,
                 highcut: float | int | None = None,
                 fs: float | int | None = None) -> None:
        """Initializes and checks parameters values.

        Args:
            lowcut (float | int | None, optional): Lowcut filter frequency in Hz. Defaults to None.
            highcut (float | int | None, optional): Highcut filter frequency in Hz. Defaults to None.
            fs (float | int | None, optional): Sampling frequency in Hz. Defaults to None.
        """
        self.lowcut = lowcut
        self.highcut = highcut
        self.sampling_frequency = fs

        self._check_params()

    def design(self,
               order: int = 5,
               output: str='ba') -> ndarray | tuple[ndarray, ndarray] | tuple[ndarray, ndarray, float]:
        """Design a Butterworth filter using scipy.butter function.

        Returns a filter with given order as given output. Identifies bandpass, lowpass or highpass
        basing on lowcut and highcut parameters.

        Args:
            order (int): Specify filter order. Defaults to 5.
            output (str): Specify in which form the output will be returned. Defaults to 'ba'.

        Returns:
            ndarray: Second-order sections representation of the IIR filter.
                Only returned if output='sos'.
            (ndarray, ndarray): Numerator (b) and denominator (a) polynomials of the IIR filter.
                Only returned if output='ba'.
            (ndarray, ndarray, float): Zeros, poles, and system gain of the IIR filter transfer function.
                Only returned if output='zpk'.
        """
        if self.lowcut and self.highcut is not None:
            return butter(order, [self.lowcut, self.highcut], fs=self.sampling_frequency, btype='band', output=output)
        elif self.lowcut is not None:
            return butter(order, self.lowcut, fs=self.sampling_frequency, btype='high', output=output)
        elif self.highcut is not None:
            return butter(order, self.highcut, fs=self.sampling_frequency, btype='low', output=output)

    def apply(self, data: ndarray | pd.Series, order: int = 5) -> ndarray:
        """Apply a Butterworth filter using scipy.sosfilt function.

        Args:
            data (ndarray): input data
            order (int, optional): Order of the Butterworth filter. Defaults to 5.

        Returns:
            ndarray: filtered data
        """
        if isinstance(data, pd.Series):
            data = data.to_numpy()

        sos = self.design(order=order, output='sos')
        output = sosfilt(sos=sos, x=data)
        return output

    def _check_params(self):
        """Method checks initialization parameters.

        Raises:
            ValueError: Cutoff frequency not specified.
            ValueError: Sampling frequency not specified.
            ValueError: Sampling frequnecy must be a positive value.
        """
        if (self.lowcut is None) and (self.highcut is None):
            raise ValueError("Cutoff frequency not specified.")
        if self.lowcut is not None and self.lowcut <=0 or self.highcut is not None and self.highcut <=0 :
            raise ValueError("Cutoff frequency must be a postivie value.")
        if self.sampling_frequency is None:
            raise ValueError("Sampling frequency not specified.")
        if self.sampling_frequency <= 0:
            raise ValueError("Sampling frequnecy must be a positive value.")