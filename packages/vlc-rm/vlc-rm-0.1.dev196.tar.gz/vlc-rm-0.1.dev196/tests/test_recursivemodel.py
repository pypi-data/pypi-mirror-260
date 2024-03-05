# Import Transmitter
from vlc_rm.transmitter import Transmitter
# Import Photodetector
from vlc_rm.photodetector import Photodetector
# Import Indoor Environment
from vlc_rm.indoorenv import Indoorenv
# Import REcursiveModel
from vlc_rm.recursivemodel import Recursivemodel
# Import Symbol Constants
from vlc_rm.constants import Constants as Kt


import numpy as np
import pytest


class TestRM:

    MIN_DC_GAIN = 2.42e-06
    MAX_DC_GAIN = 2.45e-06

    MIN_ILLUMINANCE = 1.21e+02
    MAX_ILLUMINANCE = 1.23e+02

    CHANNEL_MATRIX = np.array([
        [2.6708e-01, 5.9120e-04, 1.8104e-05],
        [4.0206e-03, 1.4772e-01, 7.7328e-02],
        [1.3841e-03, 3.6905e-02, 1.0000e+00]
        ],
        dtype=np.float32)
    
    CIE_xyz = np.array(
        [[2.3879e-01, 1.9427e-01, 5.6694e-01]],
        dtype=np.float32
        )

    CRI = np.array([[1.3921e+01]])

    transmitter = Transmitter(
            "Led1",
            position=[2.5, 2.5, 3],
            normal=[0, 0, -1],
            mlambert=1,
            wavelengths=[620, 530, 475],
            fwhm=[20, 45, 20],
            constellation='ieee16',
            luminous_flux=5000
                    )

    photodetector = Photodetector(
            "PD2",
            position=[0.5, 1.0, 0],
            normal=[0, 0, 1],
            area=1e-4,            
            fov=85,
            sensor='S10917-35GT',
            idark=1e-12
                )

    indoor_env = Indoorenv(
            "Room",
            size=[5, 5, 3],
            no_reflections=3,
            resolution=1/8,
            ceiling=[0.8, 0.8, 0.8],
            west=[0.8, 0.8, 0.8],
            north=[0.8, 0.8, 0.8],
            east=[0.8, 0.8, 0.8],
            south=[0.8, 0.8, 0.8],
            floor=[0.3, 0.3, 0.3]
                )

    indoor_env.create_environment(transmitter, photodetector)    
    
    channel_model = Recursivemodel(
        name="ChannelModelA",
        led=transmitter,
        photodetector=photodetector,
        room=indoor_env
        )
    channel_model.simulate_channel()    
    # channel_model.plot_constellation()
    print(channel_model)   

    def test_attributes(self):
        assert self.channel_model._led == self.transmitter
        assert self.channel_model._photodetector == self.photodetector
        assert self.channel_model._room == self.indoor_env

    def test_led_error(self):
        led_errors = ['a', 1, [1, 2, 3], self.photodetector]
        for options in led_errors:
            with pytest.raises(ValueError):
                channel_model = Recursivemodel(
                    "ChannelModelA",
                    options,
                    self.photodetector,
                    self.indoor_env
                    )
    
    def test_pd_error(self):
        pd_errors = ['a', 1, [1, 2, 3], self.transmitter]
        for options in pd_errors:
            with pytest.raises(ValueError):
                channel_model = Recursivemodel(
                    "ChannelModelA",
                    self.transmitter,
                    options,
                    self.indoor_env
                    )

    def test_ie_error(self):
        ie_errors = ['a', 1, [1, 2, 3], self.transmitter, self.photodetector]
        for options in ie_errors:
            with pytest.raises(ValueError):
                channel_model = Recursivemodel(
                    "ChannelModelA",
                    self.transmitter,
                    self.photodetector,
                    options
                    )

    def test_dcgain_validation(self):        
        for channel in range(Kt.NO_LEDS):
            assert self.channel_model._channel_dcgain[channel] > self.MIN_DC_GAIN
            assert self.channel_model._channel_dcgain[channel] < self.MAX_DC_GAIN

    def test_crosstalk_matrix(self):
        assert np.allclose(
            self.channel_model._norm_channelmatrix,
            self.CHANNEL_MATRIX,
            rtol=1e-4
        )

    def test_illuminance(self):
        assert self.channel_model.illuminance > self.MIN_ILLUMINANCE
        assert self.channel_model.illuminance < self.MAX_ILLUMINANCE

    def test_cie_xyz(self):
        #print(repr(self.channel_model._xyz))
        assert np.allclose(
            self.channel_model._xyz,
            self.CIE_xyz,
            rtol=1e-4
        )

    def test_cri(self):
        assert np.allclose(
            self.channel_model._cri,
            self.CRI,
            rtol=1e-4
        )

    def test_modified_option(self):
        self.photodetector.position = np.array([2.5, 2.5, 0])    
        self.indoor_env.create_environment(
            self.transmitter, 
            self.photodetector, 
            mode='modified')
        self.channel_model.simulate_channel()            
        print(self.channel_model)
        
        for channel in range(Kt.NO_LEDS):
            assert (
                self.channel_model.channel_dcgain[channel] > 4.67e-6 and                
                self.channel_model.channel_dcgain[channel] < 4.68e-6 
            )
            