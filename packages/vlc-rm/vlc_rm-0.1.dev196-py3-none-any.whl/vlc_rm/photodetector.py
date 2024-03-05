from vlc_rm.constants import Constants as Kt

# Import numpy library
import numpy as np
# Import matplot library
import matplotlib.pyplot as plt



class Photodetector:
    """
    This class defines the photodetector features

    """

    SENSORS_LIST = {
        'TCS3103-04',
        'S10917-35GT'
        }

    def __init__(
        self,
        name: str,
        position: np.ndarray,
        normal: np.ndarray,
        area: np.ndarray,
        sensor: str = " ",
        fov: float = 90,
        idark: float = 1e-12
    ) -> None:

        self._name = name

        self._position = np.array(position, dtype=np.float32)
        if self._position.size != 3:
            raise ValueError("Position must be an 1d-numpy array [x y z].")

        self._normal = np.array([normal], dtype=np.float32)
        if self._normal.size != 3:
            raise ValueError("Normal must be an 1d-numpy array [x y z].")

        self._area = np.float32(area)
        if self._area <= 0:
            raise ValueError(
                "Active area of the detector must be greater than 0.")

        self._fov = np.float32(fov)
        if self._fov <= 0 or self._fov >= 90:
            raise ValueError(
                "Field-of-View of the detector must be between 0 and 90 degrees.")

        self._sensor = sensor

        if self.sensor == 'TCS3103-04':
            # read text file into NumPy array
            self._responsivity = np.loadtxt(
                Kt.SENSOR_PATH+"ResponsivityTCS3103-04.txt")  # TODO: these files should be on a data directory
            # print("Responsivity loaded succesfully")
        elif self.sensor == 'S10917-35GT':
            self._responsivity = np.loadtxt(
                Kt.SENSOR_PATH+"ResponsivityS10917-35GT.txt")
            # print("Responsivity loaded succesfully")
        elif self.sensor == '':
            raise ValueError("Specify sensor reference")
        else:
            raise ValueError("Sensor reference not valid")

        self._idark = np.float32(idark)
        if self._idark <= 0:
            raise ValueError(
                "Dark current curve must be float and non-negative.")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def position(self) -> np.ndarray:
        return self._position

    @position.setter
    def position(self, position):        
        if self._position.size != 3:
            raise ValueError("Position must be a 3d-numpy array.")        
        self._position = np.array(position)

    @property
    def normal(self) -> np.ndarray:
        return self._normal

    @normal.setter
    def normal(self, normal):
        self._normal = np.array([normal], dtype=np.float32)
        if self._normal.size != 3:
            raise ValueError("Normal must be an 1d-numpy array [x y z].")

    @property
    def area(self) -> float:
        return self._area

    @area.setter
    def area(self, area):
        self._area = area
        if self._area <= 0:
            raise ValueError(
                "Active area of the detector must be greater than 0.0")

    @property
    def fov(self) -> float:
        return self._fov

    @fov.setter
    def fov(self, fov):
        self._fov = fov
        if self._fov <= 0 or self._fov >= 90:
            raise ValueError(
                "Field-of-View of the detector must be between 0 and 90 degrees."
                )

    @property
    def sensor(self) -> str:
        return self._sensor

    @sensor.setter
    def sensor(self, sensor) -> None:
        self._sensor = sensor

        if self.sensor == 'TCS3103-04':
            self._responsivity = np.loadtxt(
                Kt.SENSOR_PATH+"ResponsivityTCS3103-04.txt")
            print("Responsivity loaded succesfully")
        elif self.sensor == 'S10917-35GT':
            self._responsivity = np.loadtxt(
                Kt.SENSOR_PATH+"ResponsivityS10917-35GT.txt")
        else:
            raise ValueError(f"Unknown value for sensor reference{sensor}.")

    @property
    def idark(self) -> float:
        return self._idark

    @idark.setter
    def idark(self, idark):
        self._idark = idark
        if not (isinstance(self._idark, (float))) or self._idark <= 0:
            raise ValueError(
                "Dark current curve must be float and non-negative.")

    def __str__(self) -> str:
        return (
            f'\n List of parameters for photodetector {self._name}: \n'
            f'Name: {self._name} \n'
            f'Position [x y z]: {self._position} \n'
            f'Normal Vector [x y z]: {self._normal} \n'
            f'Active Area[m2]: {self._area} \n'
            f'FOV: {self._fov} \n'
            f'Sensor: {self._sensor}'
        )

    def list_sensors(self) -> None:
        """ Function to print the list of Color Shift Keying modulation formats."""
        
        print("List of Sensors available:")
        print(self.SENSORS_LIST)



    def plot_responsivity(self) -> None:
        plt.plot(
            self._responsivity[:, 0],
            self._responsivity[:, 1],
            color='r',
            linestyle='dashed'
        )
        plt.plot(
            self._responsivity[:, 0],
            self._responsivity[:, 2],
            color='g',
            linestyle='dashed'
        )
        plt.plot(
            self._responsivity[:, 0],
            self._responsivity[:, 3],
            color='b',
            linestyle='dashed'
        )
        plt.title("Spectral Responsiity of Photodetector")
        plt.xlabel("Wavelength [nm]")
        plt.ylabel("Responsivity [A/W]")
        plt.grid()
        plt.show()
