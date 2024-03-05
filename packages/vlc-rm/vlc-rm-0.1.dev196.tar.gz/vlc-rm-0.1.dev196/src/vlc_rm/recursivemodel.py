# Import Symbol Constants
from vlc_rm.constants import Constants as Kt
# Import Transmitter
from vlc_rm.transmitter import Transmitter
# Import Photodetector
from vlc_rm.photodetector import Photodetector
# Import Indoor Environment
from vlc_rm.indoorenv import Indoorenv

# Import numpy library
import numpy as np
# Library to plot SPD and responsivity
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# Library to compute color and photometry parameters
import luxpy as lx



class Recursivemodel:
    """
        This class contains the function to calculates the CIR and
        DC-gain in the optical channel and lighting parameters
    """

    def __init__(
        self,
        name: str,
        led: Transmitter,
        photodetector: Photodetector,
        room: Indoorenv
            ) -> None:

        self.name = name

        self._led = led
        if not type(self._led) is Transmitter:
            raise ValueError(
                "Tranmistter attribute must be an object type Transmitter.")

        self._photodetector = photodetector             
        if not type(photodetector) is Photodetector:
            raise ValueError(
                "Receiver attribute must be an object type Photodetector.")

        self._room = room
        if not type(self._room) is Indoorenv:
            raise ValueError(
                "Indoor environment attribute must be an object type IndoorEnv.")

        self._channel_dcgain = np.zeros((1, Kt.NO_LEDS))
        self._channelmatrix = np.zeros(
            (Kt.NO_DETECTORS, Kt.NO_LEDS),
            dtype=np.float32
            )
        self._rx_constellation = np.empty_like(self._led._constellation) 
        self._min_distance = 0  
        self._illuminance = 0
        self._cri = 0
        self._cct = 0
        self._min_distance = 0
        self._xyz = np.array((1, 3))

    @property
    def channel_dcgain(self):
        return self._channel_dcgain

    @property
    def channelmatrix(self):
        return self._channelmatrix

    @property
    def illuminance(self):
        return self._illuminance

    @property
    def cri(self):
        return self._cri

    @property
    def xyz(self):
        return self._xyz

    @property
    def cct(self):
        return self._cct
    
    @property
    def min_distance(self):
        return self._min_distance

    def __str__(self) -> str:        
        return (
            f'\n|=============== Simulation results ================|\n'
            f'Name: {self.name} \n'
            f'DC-Gain with respect to 1-W [W]: \n {self._channel_dcgain} \n'
            f'Crosstalk Matrix at {self._led._luminous_flux}-lm: \n{self._channelmatrix} \n'            
            f'Lighting Parameters at {self._led._luminous_flux}-lm \n'
            f'Illuminance [lx]: {self._illuminance} \n'
            f'CIExyz: {self._xyz} \n'
            f'CCT: {self._cct} \n'
            f'CRI: {self._cri} \n'
            f'Min-Distance: {self._min_distance} \n'
        )

    def simulate_channel(self) -> None:
        """ 
        This method simulates the indoor enviornment
        """

        print("\n Simulating indoor environment ...")
        
        self._compute_cir()
        self._compute_dcgain()
        self._create_spd()
        self._compute_cct_cri()
        self._compute_irradiance()
        self._compute_illuminance()
        self._compute_channelmatrix()
        self._compute_normalized_channelmatrix()
        self._compute_rx_constellation()
        self._compute_min_distance()
        
        print("Simulation done! \n")
        

    def print_Hk(self) -> None:
        """
        This function prints the DC-Gain for each reflection.
        """
        for i in range(0, self._room.no_reflections+1):
            print("\n DC-gain for H{} response [W] respect to 1W:\n {}".format(i, self.h_dcgain[i, :]))

    def _compute_cir(self) -> None:
        """ Function to compute the channel impulse response
            for each reflection.

        Parameters:
            led.m: lambertian number to tx emission
            led.wall_parameters: 3D array with distance and
                cosine pairwise-elemets.
            pd.area: sensitive area in photodetector


        Returns: A list with 2d-array [power_ray,time_delay] collection
            for each refletion [h_0,h_1,...,h_k].

        """

        # defing variables and arrays
        tx_index_point = self._room.no_points-2
        rx_index_point = self._room.no_points-1

        cos_phi = np.zeros(
            (self._room.no_points), dtype=np.float32)
        dis2 = np.zeros((
            self._room.no_points, self._room.no_points), dtype=np.float32)

        h0_se = np.zeros((self._room.no_points, Kt.NO_LEDS), dtype=np.float32)
        h0_er = np.zeros((self._room.no_points, 1), dtype=np.float32)

        # Time delay between source and each cells
        # h0_se[:,1] = room.wall_parameters[0,tx_index_point,:]/SPEED_OF_LIGHT
        # Time delay between receiver and each cells
        # h0_er[:,1] = room.wall_parameters[0,rx_index_point,:]/SPEED_OF_LIGHT

        # define distance^2 and cos_phi arrays
        dis2 = np.power(self._room.wall_parameters[0, :, :], 2)
        cos_phi = self._room.wall_parameters[1, int(tx_index_point), :]

        # computing the received power by each smaller area from light sooure
        tx_power = (
            (self._led.mlambert+1)/(2*np.pi) *
            np.multiply(
                np.divide(
                    1,
                    dis2[tx_index_point, :],
                    out=np.zeros((self._room.no_points)),
                    where=dis2[tx_index_point, :] != 0),
                np.power(cos_phi, self._led.mlambert)
                    )
                )

        rx_wall_factor = (
            self._photodetector._area *
            self._room.wall_parameters[1, int(rx_index_point), :]
            )

        # Differential power between all grid points without reflectance
        dP_ij = np.zeros(
            (self._room.no_points, self._room.no_points), np.float32)
        dP_ij = (
            np.divide(
                self._room.deltaA*self._room.wall_parameters[1, :, :] *
                np.transpose(self._room.wall_parameters[1, :, :]),
                np.pi * dis2, out=np.zeros_like(dP_ij),
                where=dis2 != 0
                )
            )

        # Array creation for dc_gain and previuos dc_gain
        self.h_k = []
        hlast_er = []

        # Array creation for time delay
        self.delay_hk = []
        delay_hlast_er = []

        # Time delay matrix
        tDelay_ij = np.zeros(
            (self._room.no_points, self._room.no_points), dtype=np.float32)
        tDelay_ij = self._room.wall_parameters[0, :, :]/Kt.SPEED_OF_LIGHT
        # print(np.shape(tDelay_ij))

        # TODO: check whether you can replace this for by vectorized
        # operations or comprehension operations
        for i in range(self._room.no_reflections+1):

            # Creates the array to save h_k reflections response
            # and last h_er response
            self.h_k.append(np.zeros((self._room.no_points, Kt.NO_LEDS), np.float32))
            hlast_er.append(np.zeros((self._room.no_points, Kt.NO_LEDS), np.float32))

            # Creates the array to save time-delay reflections
            # response and last h_er
            self.delay_hk.append(np.zeros(
                (self._room.no_points, 1), np.float32))
            delay_hlast_er.append(np.zeros(
                (self._room.no_points, 1), np.float32))

            if i == 0:

                # Magnitude of CIR in LoS
                self.h_k[i][0, :] = (
                    tx_power[int(rx_index_point)] *
                    rx_wall_factor[int(tx_index_point)]
                    )

                # Time Delay of CIR in LoS
                self.delay_hk[i][0, 0] = tDelay_ij[
                    int(tx_index_point), int(rx_index_point)
                        ]

            elif i == 1:
                # Impulse response between source and each cells without
                # reflectance. The reflectance is added in the h_k computing.
                h0_se = np.multiply(
                    np.reshape(
                        np.multiply(
                            self._room.deltaA * tx_power,
                            self._room.wall_parameters[
                                1, :, int(tx_index_point)]
                                ),
                        (-1, 1)
                            ),
                    self._room.reflectance_vectors
                    )

                # Impulse response between receiver and each cells
                h0_er[:, 0] = np.divide(
                    np.multiply(
                        self._room.wall_parameters[1, :, int(rx_index_point)],
                        rx_wall_factor),
                    np.pi*dis2[rx_index_point, :],
                    out=np.zeros((self._room.no_points)),
                    where=dis2[rx_index_point, :] != 0
                            )

                # print("h0_se array->:",h0_se[:,0])
                # print("h0_er array->:",h0_er[:,0])

                # Previous h_er RGBY vectors of magnitude for LoS
                hlast_er[i] = np.repeat(h0_er, repeats=Kt.NO_LEDS, axis=1)

                # Current vector for h1 impulse response for RGBY
                # Red-Green-Blue-Yellow
                self.h_k[i] = np.multiply(h0_se, hlast_er[i])

                # Time-Delay computing
                delay_hlast_er[i] = tDelay_ij[int(rx_index_point), :]
                self.delay_hk[i] = tDelay_ij[
                    int(tx_index_point), :] + delay_hlast_er[i]

                # np.savetxt(CIR_PATH+"h1.csv", h_k[i], delimiter=","

            elif i >= 2:

                # Time-Delay computing
                delay_hlast_er[i] = np.sum(
                    np.reshape(delay_hlast_er[i-1], (1, -1)) + tDelay_ij,
                    axis=1)/self._room.no_points

                self.delay_hk[i] = tDelay_ij[
                    int(tx_index_point), :] + delay_hlast_er[i]

                # Computes the last h_er to compute h_k
                for color in range(Kt.NO_LEDS):

                    hlast_er[i][:, color] = np.sum(
                        np.multiply(
                            hlast_er[i-1][:, color],
                            np.multiply(
                                self._room.reflectance_vectors[:, color], dP_ij)
                            ),
                        axis=1
                        )

                    self.h_k[i][:, color] = np.multiply(
                        h0_se[:, 0], hlast_er[i][:, color])
                    # print("h_k->",np.shape(self.h_k[i]))

    def _compute_dcgain(self) -> None:
        """
        This function calculates the total power received
        from LoS and h_k reflections
        """

        self.h_dcgain = np.zeros((self._room.no_reflections+1, Kt.NO_LEDS), np.float32)

        for i in range(0, self._room.no_reflections+1):
            self.h_dcgain[i, :] = np.sum(self.h_k[i][0:-2, 0:Kt.NO_LEDS], axis=0)

        self._channel_dcgain = np.sum(self.h_dcgain, axis=0)
        
    def _create_spd(self) -> None:
        """
        This function creates a SPD of LED from central wavelengths,
        FWHM and DC gain of channel
        """

        # Array for wavelenght points from 380nm to (782-2)nm with 2nm steps
        self.wavelenght = np.arange(380, 781, 1)

        # Numpy Array to save the spectral power distribution of each color channel
        spd_data_dcgain = np.zeros((self.wavelenght.size, Kt.NO_LEDS))

        for i in range(Kt.NO_LEDS):
            # Arrays to estimate the RGBY gain spectrum
            spd_data_dcgain[:, i] = (
                self._channel_dcgain[i] *
                self._gaussian_sprectrum(
                    self.wavelenght, 
                    self._led._wavelengths[i], 
                    self._led._fwhm[i]/2
                    )             
                )

        self._spd_data = np.multiply(
                spd_data_dcgain,
                self._led._avg_power
            )

        self._spd_total = np.sum(self._spd_data, axis=1)

    def _plot_spd(self) -> None:
        """ This function plots the SPD of QLED """
        # plot red spd data
        for i in range(Kt.NO_LEDS):
            plt.plot(self.wavelenght, self._spd_data[:, i])
        
        plt.title("Spectral Power Distribution")
        plt.xlabel("Wavelength [nm]")
        plt.ylabel("Radiometric Power [W]")
        plt.grid()
        plt.show()

    def _compute_cct_cri(self) -> None:
        """ This function calculates a CCT and CRI of the QLED SPD."""

        # Computing the xyz coordinates from SPD-RGBY estimated spectrum
        self._XYZ_uppper = lx.spd_to_xyz(
            [
                self.wavelenght,
                self._spd_total/self._photodetector.area
            ])

        # Example of xyx with D65 illuminant     
        # self._xyz = lx.spd_to_xyz(
        #    lx._CIE_ILLUMINANTS['D65']
        #    )

        self._xyz = self._XYZ_uppper/np.sum(self._XYZ_uppper)

        # Computing the CRI coordinates from SPD-RGBY estimated spectrum
        self._cri = lx.cri.spd_to_cri(
            np.vstack(
                    [
                        self.wavelenght,
                        self._spd_total/self._photodetector.area

                    ]
                )
            )
        
        # Example of CRI for D65 illuminant
        # self._cri = lx.cri.spd_to_cri(lx._CIE_ILLUMINANTS['D65'])

        # Computing the CCT coordinates from SPD-RGBY estimated spectrum
        self._cct = lx.xyz_to_cct_ohno2014(self._xyz)

    def _compute_irradiance(self) -> None:
        """ This function calculates the irradiance."""
        
        self._irradiance = lx.spd_to_power(
            np.vstack(
                [self.wavelenght, self._spd_total]
                    ),
            ptype='ru'
            )/self._photodetector._area

    def _compute_illuminance(self) -> None:
        """ This function calculates the illuminance."""
        self._illuminance = lx.spd_to_power(
            np.vstack(
                [self.wavelenght, self._spd_total]
                        ),
            ptype='pu'
            )/self._photodetector._area

    def _compute_channelmatrix(self) -> None:
        """ This function computes channel matrix."""

        for j in range(Kt.NO_LEDS):
            for i in range(Kt.NO_DETECTORS):
                self._channelmatrix[i][j] = np.dot(
                    self._spd_data[:, j], self._photodetector._responsivity[:, i+1])
    
    def _compute_normalized_channelmatrix(self) -> None:
        """ This function computes channel matrix normalized between 0 and 1."""

        self._norm_channelmatrix = self._channelmatrix/np.max(self._channelmatrix)

    def _gaussian_sprectrum(self, x, mean, std) -> np.ndarray:
        return (1 / (std * np.sqrt(2*np.pi))) * np.exp(-((x-mean)**2) / (2*std**2))
    
    def _compute_rx_constellation(self) -> None:
        """ This function computes the received constellation using the channel matrix """

        self._rx_constellation = np.dot(
            self._channelmatrix,
            self._led._constellation
            )
        # print(self._led._constellation)

    def _compute_min_distance(self) -> None:
        """ This function computes the min distance of the received constellation """

        zero_distance = self._cdist(self._rx_constellation.T, self._rx_constellation.T)
                
        self._min_distance = np.min(zero_distance[zero_distance > 0])

    def plot_constellation(self, mode='rx'):
        """ This function plots the received and transmitted constellations """    
        # Create 3D scatter plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Draw a triangle of the received constellation
        p1 = self._rx_constellation[:, np.argmax(self._rx_constellation[0, :])]
        p2 = self._rx_constellation[:, np.argmax(self._rx_constellation[1, :])]
        p3 = self._rx_constellation[:, np.argmax(self._rx_constellation[2, :])]

        ax.scatter([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], [p1[2], p2[2], p3[2]])
        # Define the vertices for the polygon
        verts = [p1, p2, p3]
        # Create the polygon
        poly = Poly3DCollection([verts], alpha=0.25, facecolor='g')
        # Add the polygon to the plot
        ax.add_collection3d(poly)

        # Draw a triangle of the transmitted
        p1 = self._led._constellation[:, np.argmax(self._led._constellation[0, :])]
        p2 = self._led._constellation[:, np.argmax(self._led._constellation[1, :])]
        p3 = self._led._constellation[:, np.argmax(self._led._constellation[2, :])]

        ax.scatter([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], [p1[2], p2[2], p3[2]])
        # Define the vertices for the polygon
        verts = [p1, p2, p3]
        # Create the polygon
        poly = Poly3DCollection([verts], alpha=0.25, facecolor='g')
        # Add the polygon to the plot
        ax.add_collection3d(poly)

        ax.scatter(
            self._rx_constellation[0, :],
            self._rx_constellation[1, :],
            self._rx_constellation[2, :]
        )
        ax.scatter(
            self._led._constellation[0, :],
            self._led._constellation[1, :],
            self._led._constellation[2, :]
        )

        # Set font size for axis labels and title
        plt.rcParams['font.size'] = 14

        # Define the coordinates for the plane
        xx, yy = np.meshgrid(range(1), range(1))
        zz = 2 * xx + 3 * yy

        # Plot the plane
        ax.plot_surface(xx, yy, zz, alpha=0.5)

        # Set limits for the axes
        ax.set_xlim3d([0, 1])
        ax.set_ylim3d([0, 1])
        ax.set_zlim3d([0, 1])
        # Add labels and title
        ax.set_xlabel('R-axis')
        ax.set_ylabel('G-axis')
        ax.set_zlabel('B-axis')
        plt.title('Constellation in Photometric Signal Space')

        # Display plot
        plt.show()

    def _cdist(self, XA, XB) -> np.ndarray:
        # Calculate the Euclidean distance between each pair of points in XA and XB
        D = np.sqrt(((XA[:, None] - XB) ** 2).sum(axis=2))

        return D