# Import Constants Transmitter
from vlc_rm.transmitter import Transmitter
# Import Constants Photodetector
from vlc_rm.photodetector import Photodetector
# Import Constants Photodetecto
from vlc_rm.indoorenv import Indoorenv


# Import Numpy
import numpy as np
# Import Pytest
import pytest


class TestIndoorEnv:

    DIST_COSINE = np.array([[
            [0.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01, 
                1.0000e+00, 0.0000e+00, 1.0000e+00],
            [7.0711e-01, 0.0000e+00, 7.0711e-01, 1.0000e+00, 7.0711e-01,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 7.0711e-01, 0.0000e+00, 7.0711e-01, 1.0000e+00,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 1.0000e+00, 7.0711e-01, 0.0000e+00, 7.0711e-01,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 7.0711e-01, 1.0000e+00, 7.0711e-01, 0.0000e+00,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [1.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                0.0000e+00, 1.0000e+00, 0.0000e+00],
            [0.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                1.0000e+00, 0.0000e+00, 1.0000e+00],
            [1.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                0.0000e+00, 1.0000e+00, 0.0000e+00]],
            [
            [0.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                1.0000e+00, 0.0000e+00, 1.0000e+00],
            [7.0711e-01, 0.0000e+00, 7.0711e-01, 1.0000e+00, 7.0711e-01,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 7.0711e-01, 0.0000e+00, 7.0711e-01, 1.0000e+00,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 1.0000e+00, 7.0711e-01, 0.0000e+00, 7.0711e-01,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 7.0711e-01, 1.0000e+00, 7.0711e-01, 0.0000e+00,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [1.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                0.0000e+00, 1.0000e+00, 0.0000e+00],
            [0.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                1.0000e+00, 0.0000e+00, 1.0000e+00],
            [1.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                0.0000e+00, 1.0000e+00, 0.0000e+00]
            ]
        ],
        dtype=np.float32)

    SIZE = [5, 5, 3]
    NO_REFLECTIONS = 3
    RESOLUTION = 1/8
    CEILING = [0.8, 0.8, 0.8]    
    WEST = [0.8, 0.8, 0.8]
    NORTH = [0.8, 0.8, 0.8]
    EAST = [0.8, 0.8, 0.8]
    SOUTH = [0.8, 0.8, 0.8]
    FLOOR = [0.3, 0.3, 0.3]

    indoorenv = Indoorenv(
        "Room",
        size=SIZE,
        no_reflections=NO_REFLECTIONS,
        resolution=RESOLUTION,
        ceiling=CEILING,
        west=WEST,
        north=NORTH,
        east=EAST,
        south=SOUTH,
        floor=FLOOR
            )    

    def test_size(self):
        assert np.array_equal(self.indoorenv.size, np.array(self.SIZE))

    def test_no_reflections(self):
        assert self.indoorenv.no_reflections == self.NO_REFLECTIONS

    def test_resolution(self):
        assert self.indoorenv.resolution == self.RESOLUTION

    def test_ceiling(self):
        assert np.array_equal(self.indoorenv.ceiling, np.array(self.CEILING))

    def test_west(self):
        assert np.array_equal(self.indoorenv.west, np.array(self.WEST))

    def test_north(self):
        assert np.array_equal(self.indoorenv.north, np.array(self.NORTH))

    def test_east(self):
        assert np.array_equal(self.indoorenv.east, np.array(self.EAST))

    def test_south(self):
        assert np.array_equal(self.indoorenv.south, np.array(self.SOUTH))

    def test_floor(self):
        assert np.array_equal(self.indoorenv.floor, np.array(self.FLOOR))

    def test_parameters(self):
        
        led1 = Transmitter(
            "Led1",
            position=[0.5, 0.5, 1],
            normal=[0, 0, -1],
            mlambert=1,
            wavelengths=[620, 530, 475],
            fwhm=[20, 45, 20],
            constellation='ieee16',
            luminous_flux=5000
                    )  

        pd1 = Photodetector(
            "PD1",
            position=[0.1, 0.1, 0],
            normal=[0, 0, 1],
            area=(1e-4),
            # area=0.5e-4,
            fov=85,
            sensor='S10917-35GT',
            idark=1e-12
                    )

        basic_env = Indoorenv(
            "Basic-Env",
            size=[1, 1, 1],
            no_reflections=3,
            resolution=1,
            ceiling=[1, 1, 1],
            west=[1, 1, 1],
            north=[1, 1, 1],
            east=[1, 1, 1],
            south=[1, 1, 1],
            floor=[1, 1, 1]
                )

        basic_env.create_environment(led1, pd1)
        print(repr(basic_env.wall_parameters))
        
        #assert np.allclose(
        #    basic_env.wall_parameters,
        #    self.DIST_COSINE
        #)
        
        pd1.position= np.array([0.5, 0.5, 0])
        basic_env.create_environment(led1, pd1, mode='modified')        
        print(repr(basic_env.wall_parameters))
        
        assert np.allclose(
            basic_env.wall_parameters,
            self.DIST_COSINE
        )
                
    def test_size_error(self):
        size_errors = [
            [1, 1], [1,  "a", "other"], [1, 1, 1, 2]
        ]
        
        for options in size_errors:
            with pytest.raises(ValueError):
                basic_env = Indoorenv(
                    "Room",
                    size=options,
                    no_reflections=self.NO_REFLECTIONS,
                    resolution=self.RESOLUTION,
                    ceiling=self.CEILING,
                    west=self.WEST,
                    north=self.NORTH,
                    east=self.EAST,
                    south=self.SOUTH,
                    floor=self.FLOOR
                    )
        
    def test_no_reflections_error(self):
        reflections_errors = [-3, 'a', 1.2, [1, 1], -3.5]

        for options in reflections_errors:
            with pytest.raises(ValueError):           
                basic_env = Indoorenv(
                    "Room",
                    size=self.SIZE,
                    no_reflections=options,
                    resolution=self.RESOLUTION,
                    ceiling=self.CEILING,
                    west=self.WEST,
                    north=self.NORTH,
                    east=self.EAST,
                    south=self.SOUTH,
                    floor=self.FLOOR
                    )
    
    def test_resolution_error(self):
        resolution_errors = [-3, 'a', 12, [1, 1], -3.5]

        for options in resolution_errors:
            with pytest.raises(ValueError):           
                basic_env = Indoorenv(
                    "Room",
                    size=self.SIZE,
                    no_reflections=self.NO_REFLECTIONS,
                    resolution=options,
                    ceiling=self.CEILING,
                    west=self.WEST,
                    north=self.NORTH,
                    east=self.EAST,
                    south=self.SOUTH,
                    floor=self.FLOOR
                    )