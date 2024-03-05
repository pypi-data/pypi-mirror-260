# Import Transmitter
from vlc_rm.transmitter import Transmitter
# Import Photodetector
from vlc_rm.photodetector import Photodetector
# Import REcursiveModel
from vlc_rm.constants import Constants as Kt

# import numpy library
import numpy as np


class Indoorenv:
    """
    This class defines the indoor environment features, and computes
    the points grid and the cosine and distance pair-waise.

    """

    def __init__(
        self,
        name: str,
        size: np.ndarray,
        resolution: float,
        ceiling: np.ndarray,
        west: np.ndarray,
        north: np.ndarray,
        east: np.ndarray,
        south: np.ndarray,
        floor: np.ndarray,
        no_reflections: int = 3        
    ) -> None:

        self._name = name
        self.deltaA = 'Non defined, create grid.'
        self.no_points = 'Non defined, create grid.'

        self._size = np.array(size, dtype=np.float32)
        if self._size.size != 3:
            raise ValueError(
                "Size of the indoor environment must be an 1d-numpy array [x y z]")        

        self._no_reflections = no_reflections
        if not isinstance(self._no_reflections, int):
            raise ValueError(
                "No of reflections must be a positive integer between 0 and 10.")
        if self._no_reflections < 0 or self._no_reflections > 10:
            raise ValueError(
                "No of reflections must be a real integer between 0 and 10.")
        
        self._resolution = np.float32(resolution)
        if self._resolution > min(self._size):
            raise ValueError(
                "Resolution of points must be less or equal to minimum size of the rectangular indoor space.")
        if self._resolution <= 0:
            raise ValueError(
                "Resolution of points must be a real number greater than zero.")

        self._ceiling = np.array(ceiling)
        if self._ceiling.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of ceiling reflectance array must be equal to the number of LEDs.")

        self._west = np.array(west)
        if self._west.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of north reflectance array must be equal to the number of LEDs.")
                        
        self._north = np.array(north)
        if self._north.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of north reflectance array must be equal to the number of LEDs.")
        
        self._east = np.array(east)
        if self._east.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of east reflectance array must be equal to the number of LEDs.")

        self._south = np.array(south)
        if self._south.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of south reflectance array must be equal to the number of LEDs.")

        self._floor = np.array(floor)
        if self._floor.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of floor reflectance array must be equal to the number of LEDs.")

    @property
    def name(self):
        """The name property"""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def size(self) -> np.ndarray:
        """The size property"""
        return self._size

    @size.setter
    def size(self, size):
        self._size = np.array(size)
        if self._size.size != 3:
            raise ValueError(
                "Size of the indoor environment must be an 1d-numpy array [x y z]")

    @property
    def no_reflections(self) -> int:
        """The number of reflections property"""
        return self._no_reflections

    @no_reflections.setter
    def no_reflections(self, no_reflections):
        self._no_reflections = no_reflections
        if self._no_reflections <= 0:
            raise ValueError(
                "Resolution of points must be a real integer between 0 and 10.")

    @property
    def resolution(self) -> float:
        """The resolution property"""
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        self._resolution = resolution
        if self._resolution <= 0:
            raise ValueError(
                "Resolution of points must be a real number greater than zero.")

    @property
    def ceiling(self) -> np.ndarray:
        """The ceiling property"""
        return self._ceiling

    @ceiling.setter
    def ceiling(self, ceiling):
        self._ceiling = np.array(ceiling)
        if self._ceiling.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of ceiling reflectance array must be equal to the number of LEDs.")

    @property
    def west(self) -> np.ndarray:
        """The west property"""
        return self._west

    @west.setter
    def west(self, west):
        self._west = np.array(west)
        if self._ceiling.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of west reflectance array must be equal to the number of LEDs.")

    @property
    def north(self) -> np.ndarray:
        """The north property"""
        return self._north

    @north.setter
    def north(self, north):
        self._north = np.array(north)
        if self._north.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of north reflectance array must be equal to the number of LEDs.")

    @property
    def east(self) -> np.ndarray:
        """The east property"""
        return self._east

    @east.setter
    def east(self, east):
        self._east = np.array(east)
        if self._east.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of east reflectance array must be equal to the number of LEDs.")

    @property
    def south(self) -> np.ndarray:
        """The east property"""
        return self._south

    @south.setter
    def south(self, south):
        self._south = np.array(south)
        if self._south.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of south reflectance array must be equal to the number of LEDs.")

    @property
    def floor(self) -> np.ndarray:
        """The floor property"""
        return self._floor

    @floor.setter
    def floor(self, floor):
        self._floor = np.array(floor)
        if self._floor.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of ceiling reflectance array must be equal to the number of LEDs.")


    
    def __str__(self) -> str:
        return (
            f'\n List of parameters for indoor envirionment {self._name}: \n'
            f'Name: {self._name}\n'
            f'Size [x y z] -> [m]: {self._size} \n'
            f'Order reflection: {self._no_reflections} \n'
            f'Resolution points [m]: {self._resolution}\n'
            f'Smaller Area [m^2]: {self.deltaA}\n'
            f'Number of points: {self.no_points}\n'
        )    

    def create_environment(
        self,
        tx: Transmitter,
        rx: Photodetector,
        mode: str = 'new'
            ) -> None:

        self._tx = tx
        if not type(self._tx) is Transmitter:
            raise ValueError(
                "Tranmistter attribute must be an object type Transmitter.")

        self._rx = rx
        if not type(self._rx) is Photodetector:
            raise ValueError(
                "Receiver attribute must be an object type Photodetector.")
        
        if (mode != 'new') and (mode != 'modified'):
            raise ValueError(
                "Mode attribute must be 'new' or 'modified'.")

        print("\n Creating parameters of indoor environment ...")

        self._create_grid(
            self._tx._position,
            self._rx._position,
            self._tx._normal,
            self._rx._normal
            )
        
        self._compute_parameters(self._rx._fov, mode)
        print("Parameters created!\n")

    def _create_grid(
        self,
        tx_position: np.ndarray,
        rx_position: np.ndarray,
        tx_normal: np.ndarray,
        rx_normal: np.ndarray
    ) -> None:
        """ This function creates a grid of points on every wall. """

        no_xtick = int(self._size[0]/self._resolution)
        no_ytick = int(self._size[1]/self._resolution)
        no_ztick = int(self._size[2]/self._resolution)

        ceiling_points = np.zeros((no_xtick*no_ytick, 3), dtype=np.float16)
        west_points = np.zeros((no_ztick*no_xtick, 3), dtype=np.float16)
        north_points = np.zeros((no_ztick*no_ytick, 3), dtype=np.float16)
        east_points = np.zeros((no_ztick*no_xtick, 3), dtype=np.float16)
        south_points = np.zeros((no_ztick*no_ytick, 3), dtype=np.float16)
        floor_points = np.zeros((no_xtick*no_ytick, 3), dtype=np.float16)

        ceiling_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[0]], no_xtick*no_ytick, axis=0)
        east_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[1]], no_ztick*no_xtick, axis=0)
        south_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[2]], no_ztick*no_ytick, axis=0)
        west_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[3]], no_ztick*no_xtick, axis=0)
        north_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[4]], no_ztick*no_ytick, axis=0)
        floor_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[5]], no_xtick*no_ytick, axis=0)

        # Creates reflectance vector for each point
        ceiling_reflectance = np.repeat(
            [self._ceiling], no_xtick*no_ytick, axis=0)
        west_reflectance = np.repeat(
            [self._west], no_ztick*no_xtick, axis=0)
        north_reflectance = np.repeat(
            [self._north], no_ztick*no_ytick, axis=0)
        east_reflectance = np.repeat(
            [self._east], no_ztick*no_xtick, axis=0)
        south_reflectance = np.repeat(
            [self._south], no_ztick*no_ytick, axis=0)
        floor_reflectance = np.repeat(
            [self._floor], no_xtick*no_ytick, axis=0)

        x_ticks = np.linspace(
            self._resolution/2, self._size[0]-self._resolution/2, no_xtick)
        y_ticks = np.linspace(
            self._resolution/2, self._size[1]-self._resolution/2, no_ytick)
        z_ticks = np.linspace(
            self._resolution/2, self._size[2]-self._resolution/2, no_ztick)

        self.no_points = (
            2*no_xtick*no_ytick +
            2*no_ztick*no_xtick +
            2*no_ztick*no_ytick + 2)

        # Generates the x,y,z of grids in each points
        x_ygrid, y_xgrid = np.meshgrid(x_ticks, y_ticks)
        x_zgrid, z_xgrid = np.meshgrid(x_ticks, z_ticks)
        y_zgrid, z_ygrid = np.meshgrid(y_ticks, z_ticks)

        # Save x,y,z coordinates of points in each wall
        ceiling_points[:, 0] = floor_points[:, 0] = x_ygrid.flatten()
        ceiling_points[:, 1] = floor_points[:, 1] = y_xgrid.flatten()
        ceiling_points[:, 2], floor_points[:, 2] = self._size[2], 0

        west_points[:, 0] = east_points[:, 0] = x_zgrid.flatten()
        west_points[:, 2] = east_points[:, 2] = z_xgrid.flatten()
        east_points[:, 1], west_points[:, 1] = 0, self._size[1]

        north_points[:, 1] = south_points[:, 1] = y_zgrid.flatten()
        north_points[:, 2] = south_points[:, 2] = z_ygrid.flatten()
        south_points[:, 0], north_points[:, 0] = 0, self._size[0]

        # Creates tensors for gridpoints,
        # normal vectors and reflectance vectors.
        self.gridpoints = np.concatenate((
            ceiling_points,
            east_points,
            south_points,
            west_points,
            north_points,
            floor_points,
            [tx_position],
            [rx_position]),
            axis=0
        )

        self.normal_vectors = np.concatenate((
            ceiling_normal,
            east_normal,
            south_normal,
            west_normal,
            north_normal,
            floor_normal,
            tx_normal,
            rx_normal),
            axis=0, dtype=np.float16)

        self.reflectance_vectors = np.concatenate((
            ceiling_reflectance,
            east_reflectance,
            south_reflectance,
            west_reflectance,
            north_reflectance,
            floor_reflectance,
            np.zeros((1, Kt.NO_LEDS)),
            np.zeros((1, Kt.NO_LEDS))),
            axis=0, dtype=np.float16)

        self.deltaA = (
            2*self._size[0]*self._size[1] +
            2*self._size[0]*self._size[2] +
            2*self._size[1]*self._size[2]
        )/(self.no_points-2)

    def _compute_parameters(self, fov: float, mode) -> None:
        """This function creates an 3d-array with cross-parametes between
            points.

        This parameters are the distance between points and the cosine of the
        angles respect to the normal vector. Using this array is commputed the
        channel immpulse response.

        Parameters:
            gridpoints: 2d tensor array with [x,y,z] coordinates for each point
            normal_vector: 2d tensor array with [x,y,z] coordinates of normal
                vector in each point

        Returns: Returns a 3d-array with distance and cos(tetha) parameters.
            The shape of this array is [2,no_points,no_points].


            _____________________
           /                    /|
          /                    / |
         /                    /  |
        /____________________/  /|
        |     Distance       | / |
        |____________________|/ /
        |     Cos(tetha)     | /
        |____________________|/


        """

        if mode == 'new':
            self.wall_parameters = np.zeros(
                (2, self.no_points, self.no_points), dtype=np.float32)

            # Computes pairwise-element distance using tensor
            # TODO: consider using Numpy only if possible
            # dist = scipy.spatial.distance.cdist(self.gridpoints, self.gridpoints)        
            distances = np.linalg.norm(self.gridpoints[:, np.newaxis, :] - self.gridpoints[np.newaxis, :, :], axis=2)

            # Computes the pairwise-difference (vector) using tensor
            diff = -np.expand_dims(self.gridpoints, axis=1) + self.gridpoints

            # Computes the unit vector from pairwise-difference usiing tensor
            unit_vector = np.divide(
                diff,
                np.reshape(distances, (self.no_points, self.no_points, 1)),
                np.zeros_like(diff),
                where=np.reshape(distances, (self.no_points, self.no_points, 1)) != 0
                )

            # Computes the cosine of angle between unit vector and
            # normal vector using tensor.
            cos_phi = np.sum(
                unit_vector*np.reshape(
                    self.normal_vectors,
                    (self.no_points, 1, 3)),
                axis=2
                )

            array_rx = cos_phi[-1, :]
            low_values_flags = array_rx < np.cos(fov*np.pi/180)
            array_rx[low_values_flags] = 0

            array_tx = cos_phi[-2, :]
            low_values_flags = array_tx < np.cos(90*np.pi/180)
            array_tx[low_values_flags] = 0

            # Save in numpy array the results of tensor calculations
            self.wall_parameters[0, :, :] = distances
            self.wall_parameters[1, :, :] = cos_phi
        
        elif mode == 'modified':

            tx_diff = self.gridpoints - self.gridpoints[-2, :]
            rx_diff = self.gridpoints - self.gridpoints[-1, :]

            tx_distance = np.linalg.norm(tx_diff, axis=1)
            rx_distance = np.linalg.norm(rx_diff, axis=1)

            tx_unit_vector = np.divide(
                tx_diff,
                np.reshape(tx_distance, (self.no_points, 1)),
                np.zeros_like(tx_diff),
                where=np.reshape(tx_distance, (self.no_points, 1)) != 0
                )

            rx_unit_vector = np.divide(
                rx_diff,
                np.reshape(rx_distance, (self.no_points, 1)),
                np.zeros_like(rx_diff),
                where=np.reshape(rx_distance, (self.no_points, 1)) != 0
                )
            
            tx_cos_phi = np.dot(
                tx_unit_vector,
                self.normal_vectors[-2, :].T
                )
            
            rx_cos_phi = np.dot(
                rx_unit_vector,
                self.normal_vectors[-1, :].T
                )
                
            tx_wall_cos_theta = np.sum(
                np.multiply(
                    -tx_unit_vector,
                    self.normal_vectors
                ),
                axis=1
            )

            rx_wall_cos_theta = np.sum(
                np.multiply(
                    -rx_unit_vector,
                    self.normal_vectors
                ),
                axis=1
            )

            array_rx = rx_cos_phi
            low_values_flags = array_rx < np.cos(fov*np.pi/180)
            array_rx[low_values_flags] = 0

            array_tx = tx_cos_phi
            low_values_flags = array_tx < np.cos(90*np.pi/180)
            array_tx[low_values_flags] = 0

            self.wall_parameters[0, -2, :] = tx_distance            
            self.wall_parameters[0, -1, :] = rx_distance
            self.wall_parameters[0, :, -2] = tx_distance
            self.wall_parameters[0, :, -1] = rx_distance

            self.wall_parameters[1, -2, :] = tx_cos_phi
            self.wall_parameters[1, -1, :] = rx_cos_phi
            self.wall_parameters[1, :, -2] = tx_wall_cos_theta
            self.wall_parameters[1, :, -1] = rx_wall_cos_theta

            # print(tx_cos_phi, rx_cos_phi)
            # print(tx_distance, rx_distance)