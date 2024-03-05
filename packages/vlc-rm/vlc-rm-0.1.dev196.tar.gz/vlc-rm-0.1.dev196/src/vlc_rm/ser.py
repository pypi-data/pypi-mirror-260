from vlc_rm.constants import Constants as Kt
# Import REcursiveModel
from vlc_rm.recursivemodel import Recursivemodel

# Numeric Numpy library
import numpy as np
# Library to compute color and photometry parameters
import luxpy as lx
# Library to plot SER
import matplotlib.pyplot as plt



class SymbolErrorRate:
    """
    This class defines the transmitter features
    """

    def __init__(
        self,
        name: str,
        recursivemodel: Recursivemodel,        
        no_symbols: int
            ) -> None:

        if isinstance(no_symbols, (int, float)):
            self._no_symbols = int(no_symbols)        
        else:
            raise ValueError(
                "No of symbols must be a positive integer.")
        
        if self._no_symbols <= 0:
            raise ValueError(
                "No. of symbols must be greater than zero.")

        self._recursivemodel = recursivemodel
        if not type(self._recursivemodel) is Recursivemodel:
            raise ValueError(
                "Recursivemodel attribute must be an object type Recursivemodel.")        

    @property
    def no_symbols(self) -> int:
        """The number of symbols for the transmission"""
        return self._no_symbols

    @no_symbols.setter
    def no_symbols(self, no_symbols):
        if isinstance(no_symbols, (int, float)):
            self._no_symbols = int(no_symbols)        
        else:
            raise ValueError(
                "No of symbols must be a positive integer.")
        
        if self._no_symbols <= 0:
            raise ValueError(
                "No. of symbols must be greater than zero.")

    def compute_ser_flux(
            self,
            min_flux: float = 1,
            max_flux: float = 50,
            points_flux: int = 10        
            ) -> None:
        """
        This function simulates the transmission of the CSK by changing 
        the luminous flux radiated by the light source. The user uses 
        this function, which bundles four main methods. 
        """

        self._min_flux = min_flux
        if not (isinstance(self._min_flux, (int, float))) or self._min_flux <= 0:
            raise ValueError(
                "Minimum value of luminous flux must be non-negative int or float.")

        self._max_flux = max_flux
        if not (isinstance(self._max_flux, (int, float))) or self._max_flux <= 0:
            raise ValueError(
                "Maximum value of luminous flux must be non-negative int or float.")
        elif self._max_flux <= self._min_flux:
            raise ValueError(
                "Maximum value of luminouns flux must be greater than Minimum Flux.")

        self._points_flux = points_flux
        if not (isinstance(self._points_flux, (int))) or self._points_flux <= 0:
            raise ValueError(
                "Points for SER curve must be int and non-negative.")            

        print("\n Computing the Symbol Error Rate curves ...")      
        
        self._create_symbols()
        self._transmit_symbols()
        self._compute_ser_curve(mode="flux")

        print("SER computation done!\n")

    def compute_ser_snr(
            self,
            min_snr: float = 0,
            max_snr: float = 50,
            points_snr: int = 10
            ) -> None:
        """
        This function simulates the transmission of the CSK by changing 
        the signal to noise ratio. The user uses this function, which 
        bundles four main methods. 
        """
        self._min_snr = min_snr
        if not (isinstance(self._min_snr, (int, float))):
            raise ValueError(
                "Minimum value of SNR must be int or float.")

        self._max_snr = max_snr
        if not (isinstance(self._max_snr, (int, float))):
            raise ValueError(
                "Maximum value of SNR must be int or float.")
        elif self._max_snr <= self._min_snr:
            raise ValueError(
                "Maximum value of SNR must be greater than Minimum SNR.")

        self._points_snr = points_snr
        if not (isinstance(self._max_snr, (int))) or self._points_snr <= 0:
            raise ValueError(
                "Points for SER curve must be int and non-negative.")
        
        self._create_symbols()
        self._transmit_symbols()
        self._compute_ser_curve("snr")

    def plot_ser(self, mode) -> None:
        """
        This function plots the Symbol Error Rate curve
        """
        if mode=='snr':
            # convert y-axis to Logarithmic scale
            plt.yscale("log")
            plt.plot(
                self._snr_values,
                self._ser_values,
                color='b',
                linestyle='dashed'
            )
            plt.title("Symbol Error Rate")
            plt.xlabel("Signal to Noise Ration [dB]")
            plt.ylabel("Error Probability")
            plt.grid()
            plt.show()
        elif mode=='flux':
            # convert y-axis to Logarithmic scale
            plt.yscale("log")
            plt.plot(
                self._flux_values,
                self._ser_values,
                color='b',
                linestyle='dashed'
            )
            plt.title("Symbol Error Rate")
            plt.xlabel("Luminous Flux [lm]")
            plt.ylabel("Error Probability")
            plt.grid()
            plt.show()
        else:
            raise ValueError(
                "Mode for plottig SER curve is not valid.")

    def save_to_file(self, name: str = 'SER-Flux') -> None:
        """
        This function save in txt the numpy arrays with the
        symbol erro rate data.
        """

        np.savetxt(
            f'{name}.txt',
            (self._flux_values, self._ser_values),
            delimiter=' '
            )

    def _create_symbols(self) -> None:
        """
        This function creates the symbols array to transmit.
        """
        # create a random symbols identifier (decimal) for payload
        self._symbols_decimal = np.random.randint(
                0,
                self._recursivemodel._led._order_csk-1,
                (self._no_symbols),
                dtype='int16'
            )

        self._symbols_payload = np.zeros((Kt.NO_LEDS, self._no_symbols))

        self._constellation = self._recursivemodel._led._constellation
        
        for index, counter in zip(self._symbols_decimal, range(self._no_symbols)):
                self._symbols_payload[:, counter] = self._constellation[:, index]

        # Define the number of symbols for delimiter header
        self._delimiter_set = 3

        # add to the payload three base-set of symbols
        self._symbols_csk = np.concatenate((
                np.identity(Kt.NO_LEDS),
                np.identity(Kt.NO_LEDS),
                np.identity(Kt.NO_LEDS),
                self._symbols_payload),
                axis=1
            )

    def _transmit_symbols(self) -> None:       
        """ This function computes the channel transformation of the
        original symbols.
        """

        self._symbols_rx_1lm = np.matmul(
            np.matmul(
                self._recursivemodel.channelmatrix,
                self._recursivemodel._led._iler_matrix
                ),
            self._symbols_csk
            )

    def _add_noise(self, target_snr_db) -> None:
        """ 
        This function adds AWGN noise to the self._symbols_rx_1lm
        array.
        """

        # plt.stem(self._symbols_rx_1lm[0, :])
        # plt.show()

        # Create an empty numpy-array equal to self._symbols_rx_1lm
        self._noise_symbols = np.empty_like(self._symbols_rx_1lm)

        for color_channel in range(Kt.NO_DETECTORS):
            # define the x_current signal to add AWGN 
            x_current = self._symbols_rx_1lm[color_channel, :]
            # Calculate the power of the signal in the color channel
            x_watts = x_current ** 2
            # Calculate signal power and convert to dB 
            sig_avg_watts = np.mean(x_watts)
            sig_avg_db = 10 * np.log10(sig_avg_watts)
            # Calculate noise according to [2] then convert to watts
            noise_avg_db = sig_avg_db - target_snr_db
            noise_avg_watts = 10 ** (noise_avg_db / 10)
            # Generate an sample of white noise
            mean_noise = 0        
            noise_current = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(x_watts))
            # Noise up the original signal
            signal_noise = x_current + noise_current
            # Convert negative values to zero
            signal_noise[signal_noise < 0] = 0
            # Save signal with noise in array
            self._noise_symbols[color_channel, :] = signal_noise

    def _add_dark_current(self, flux, idark) -> None:
        """ This function adds dark current to the photodetected current """

        # Create an empty numpy-array equal to self._symbols_rx_1lm
        self._noise_symbols = np.empty_like(self._symbols_rx_1lm)

        for color_channel in range(Kt.NO_DETECTORS):
            # define the x_current signal to add AWGN 
            x_current = self._symbols_rx_1lm[color_channel, :]            
            # Equal the standard deviation to dark current
            std_deviation = idark
            # Generate an sample of white noise
            mean_noise = 0
            noise_current = np.random.normal(mean_noise, std_deviation, len(x_current))
            # Noise up the original signal
            signal_noise = flux*x_current + noise_current
            # Save signal with noise in array
            self._noise_symbols[color_channel, :] = signal_noise

    def _decode_symbols(self):
        """
        This funtion decodes the CSK symbols from the self._noise_symbols
        """

        # get the header and payload of the noisy received symbols
        self._rx_header = self._noise_symbols[:, 0:Kt.NO_DETECTORS*self._delimiter_set]
        self._rx_payload = self._noise_symbols[:, Kt.NO_DETECTORS*self._delimiter_set:]

        # split the header into base-set
        bases_split = np.array(
            np.array_split(
                self._rx_header,
                self._delimiter_set,
                axis=1
                )
            )

        # average of the base-sets
        avg_bases = np.mean(
            bases_split,
            axis=0
            )
        
        # computes the inverse channel matrix from transmitted header
        self._rx_channel_inverse = np.linalg.inv(avg_bases)

        # apply the inverse matrix for decoding
        self._inverse_rx_symbols = np.matmul(
                self._rx_channel_inverse,
                self._rx_payload
            )

        # Distance between constellation and received                        
        self._distance = self._cdist(
                np.transpose(self._inverse_rx_symbols),
                np.transpose(self._constellation)
                )        

        self._index_min = np.empty_like(self._symbols_decimal)

        for symbol in range(self._no_symbols):
            self._index_min[symbol] = np.argmin(self._distance[symbol])

    def _compute_error_rate(self) -> float:
        """
        This function computes the symbol error rate 
        """

        # count different values and divide above the number of symbols        
        return np.count_nonzero(self._symbols_decimal != self._index_min)/self._no_symbols

    def _compute_ser_curve(self, mode) -> None:
        """
        This function create a symbol error rate curve  
        """
        if mode == 'flux':
            self._flux_values = np.linspace(self._min_flux, self._max_flux, self._points_flux+1)
            self._ser_values = np.empty_like(self._flux_values)

            for flux, index in zip(self._flux_values, range(len(self._flux_values))):
                self._add_dark_current(flux, self._recursivemodel._photodetector._idark)
                self._decode_symbols()
                self._ser_values[index] = self._compute_error_rate()

        elif mode == 'snr':
            self._snr_values = np.linspace(self._min_snr, self._max_snr, self._points_snr+1)
            self._ser_values = np.empty_like(self._snr_values)

            for snr, index in zip(self._snr_values, range(len(self._snr_values))):
                self._add_noise(snr)
                self._decode_symbols()
                self._ser_values[index] = self._compute_error_rate()
        else:
            raise ValueError(
                "Mode for SER curve is not valid.")
    
    def _cdist(self, XA, XB) -> np.ndarray:
        # Calculate the Euclidean distance between each pair of points in XA and XB
        D = np.sqrt(((XA[:, None] - XB) ** 2).sum(axis=2))

        return D
    
    def __str__(self) -> str:
        return (
            f'\n|============= Error Rate analysis ==============|\n'
            f'\n List of parameter of SER object \n'
            f'Number of symbols: {self._no_symbols} \n'
            f'Min Flux [lm]: {self._min_flux} \n'
            f'Max Flux [lm]: {self._max_flux} \n'
        )
