# Import Transmitter
from vlc_rm.transmitter import Transmitter
# Import Photodetector
from vlc_rm.photodetector import Photodetector
# Import Indoor Environment
from vlc_rm.indoorenv import Indoorenv
# Import REcursiveModel
from vlc_rm.recursivemodel import Recursivemodel
# Import SER 
from vlc_rm.ser import SymbolErrorRate
# Import Symbol Constants
from vlc_rm.constants import Constants as Kt

import numpy as np
import pytest


class TestSER:

    SER_VALUES = np.array(
            [9.6921e-01, 3.2325e-01, 9.5142e-02, 1.5848e-02, 1.4954e-03,
             1.1980e-04, 8.8000e-06, 2.0000e-07, 0.0000e+00]
            )

    FLUX_VALUES = np.array(
        [1.0000e+01, 1.2588e+03, 2.5075e+03, 3.7562e+03, 5.0050e+03,
       6.2538e+03, 7.5025e+03, 8.7512e+03, 1.0000e+04]
    )
    
    NO_SYMBOLS = 16

    led1 = Transmitter(
        "Led1",
        position=[2.5, 2.5, 3],
        normal=[0, 0, -1],
        mlambert=1,
        wavelengths=[620, 530, 475],
        fwhm=[20, 45, 20],
        constellation='ieee16',
        luminous_flux=5000
                )  

    pd1 = Photodetector(
        "PD2",
        position=[1.5, 1.5, 0.85],
        normal=[0, 0, 1],
        area=(1e-6)/3,
        # area=0.5e-4,
        fov=85,
        sensor='S10917-35GT',
        idark=1e-12
                )    

    room = Indoorenv(
        "Room",
        size=[5, 5, 3],
        no_reflections=10,
        resolution=1/8,
        ceiling=[0.82, 0.71, 0.64],
        west=[0.82, 0.71, 0.64],
        north=[0.82, 0.71, 0.64],
        east=[0.82, 0.71, 0.64],
        south=[0.82, 0.71, 0.64],
        floor=[0.635, 0.61, 0.58]
            )
    room.create_environment(led1, pd1)
    
    channel_model = Recursivemodel("ChannelModelA", led1, pd1, room)
    channel_model.simulate_channel()
    
    ser = SymbolErrorRate(
            "SER-1",
            recursivemodel=channel_model,
            no_symbols=NO_SYMBOLS
            )
    
    def test_attributes(self):
        assert self.ser._recursivemodel == self.channel_model
        assert self.ser.no_symbols == self.NO_SYMBOLS

    def test_ser_validation(self):        
        self.ser.compute_ser_flux(
            min_flux=10,
            max_flux=10e3,
            points_flux=8
            )
        
        #print(repr(self.ser._flux_values))                     
        #print(repr(self.ser._ser_values))                    

        assert np.allclose(
            self.ser._flux_values,
            self.FLUX_VALUES,
            rtol=1e-4
                )
        
        assert min(self.ser._ser_values) < 1e-6

    
    def test_rm_error(self):
        rm_errors = ['a', 1, [1, 2, 3], self.led1, self.pd1]

        for options in rm_errors:
            with pytest.raises(ValueError):
                ser_wrong = SymbolErrorRate(
                    "SER-1",
                    recursivemodel=options,
                    no_symbols=1e6
                    )
    
    def test_no_symbols_error(self):
        rm_errors = ['a', -10, [1, 2, 3], self.led1, self.pd1]

        for options in rm_errors:
            with pytest.raises(ValueError):
                ser_wrong = SymbolErrorRate(
                    "SER-1",
                    recursivemodel=self.channel_model,
                    no_symbols=options
                    )
            with pytest.raises(ValueError):
                self.ser.no_symbols = options

    def test_min_flux_error(self):
        min_flux_errors = ['a', 'other', [1, 1, 1], 20e3]
        for options in min_flux_errors:
            with pytest.raises(ValueError):
                self.ser.compute_ser_flux(
                    min_flux=options,
                    max_flux=10e3,
                    points_flux=8
                    )

    def test_max_flux_error(self):
        max_flux_errors = ['a', 'other', [1, 1, 1], 1]
        for options in max_flux_errors:
            with pytest.raises(ValueError):
                self.ser.compute_ser_flux(
                    min_flux=10,
                    max_flux=options,
                    points_flux=8
                    )

    def test_points_flux_error(self):
        points_flux_errors = ['a', 'other', [1, 1, 1], -10]
        for options in points_flux_errors:
            with pytest.raises(ValueError):
                self.ser.compute_ser_flux(
                    min_flux=10,
                    max_flux=10e3,
                    points_flux=options
                    )

    def test_min_snr_error(self):
        min_snr_errors = ['a', 'other', [1, 1, 1], 20e3]
        for options in min_snr_errors:
            with pytest.raises(ValueError):
                self.ser.compute_ser_snr(
                    min_snr=options,
                    max_snr=10e3,
                    points_snr=8
                    )

    def test_max_snr_error(self):
        max_snr_errors = ['a', 'other', [1, 1, 1], 1]
        for options in max_snr_errors:
            with pytest.raises(ValueError):
                self.ser.compute_ser_snr(
                    min_snr=10,
                    max_snr=options,
                    points_snr=8
                    )

    def test_points_snr_error(self):
        points_snr_errors = ['a', 'other', [1, 1, 1], -10]
        for options in points_snr_errors:
            with pytest.raises(ValueError):
                self.ser.compute_ser_snr(
                    min_snr=10,
                    max_snr=10e3,
                    points_snr=options
                    )
                    