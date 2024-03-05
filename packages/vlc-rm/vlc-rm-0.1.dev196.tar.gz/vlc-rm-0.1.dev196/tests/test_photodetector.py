# Import Photodetector
from vlc_rm.photodetector import Photodetector
# Import Numpy
import numpy as np
# Import Pytest
import pytest


class TestPhotodetector:

    POSITION = [6.6, 2.8, 0.8]
    NORMAL = [0, 0, 1]
    AREA = 1e-4
    FOV = 70
    SENSOR = 'S10917-35GT'
    IDARK = 1e-12

    photodetector = Photodetector(
        "PD1",
        position=POSITION,
        normal=NORMAL,
        area=AREA,
        fov=FOV,
        sensor=SENSOR,
        idark=IDARK
            )
    
    def test_position(self):
        assert np.array_equal(
            self.photodetector.position,
            np.array(self.POSITION, dtype=np.float32)
            )

    def test_normal(self):
        assert np.array_equal(self.photodetector.normal, np.array([self.NORMAL]))

    def test_area(self):
        assert self.photodetector.area == np.float32(self.AREA)

    def test_fov(self):
        assert self.photodetector.fov == self.FOV

    def test_sensor(self):
        assert self.photodetector.sensor == self.SENSOR

    def test_idark(self):
        assert self.photodetector.idark == np.float32(self.IDARK)    

    def test_position_error(self):
        position_errors = [[0, 1], ['a', 0.5, 0], 'a', 'other', [1, 2, 3, 4]]

        for options in position_errors:
            with pytest.raises(ValueError):
                photodetector = Photodetector(
                    "PD1",
                    position=options,
                    normal=self.NORMAL,
                    area=self.AREA,
                    fov=self.FOV,
                    sensor=self.SENSOR,
                    idark=self.IDARK
                        )

    def test_normal_error(self):
        normal_errors = [[0, 1], ['a', 0.5, 0], 'a', 'other', [1, 2, 3, 4]]
        for options in normal_errors:
            with pytest.raises(ValueError):
                photodetector = Photodetector(
                    "PD1",
                    position=self.POSITION,
                    normal=options,
                    area=self.AREA,
                    fov=self.FOV,
                    sensor=self.SENSOR,
                    idark=self.IDARK
                        )       
    
    def test_fov_error(self):
        fov_errors = [-20, 200, [0, 1], ['a', 0.5, 0], 'a', 'other', [1, 2, 3, 4]]

        for options in fov_errors:
            with pytest.raises(ValueError):
                photodetector = Photodetector(
                    "PD1",
                    position=self.POSITION,
                    normal=self.NORMAL,
                    area=self.AREA,
                    fov=options,
                    sensor=self.SENSOR,
                    idark=self.IDARK
                        )        

    def test_sensor_error(self):
        sensor_errors = [-20, 200, [0, 1], ['a', 0.5, 0], 'a', 'other', [1, 2, 3, 4]]

        for options in sensor_errors:
            with pytest.raises(ValueError):
                photodetector = Photodetector(
                    "PD1",
                    position=self.POSITION,
                    normal=self.NORMAL,
                    area=self.AREA,
                    fov=self.FOV,
                    sensor=options,
                    idark=self.IDARK
                        )        
    
    def test_idark_error(self):
        idark_errors = [-1, -1e-6, 'a', [1, 1]]

        for options in idark_errors:
            with pytest.raises(ValueError):
                photodetector = Photodetector(
                    "PD1",
                    position=self.POSITION,
                    normal=self.NORMAL,
                    area=self.AREA,
                    fov=self.FOV,
                    sensor=self.SENSOR,
                    idark=options
                        )
