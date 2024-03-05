# Import Transmitter module
from vlc_rm.transmitter import Transmitter
# Import Constant module
from vlc_rm.constants import Constants as Kt
# Import Numpy
import numpy as np
# Import Pytest
import pytest



class TestTransmitter:    

    SYMBOLS_CONSTELLATION = np.transpose(
        np.array([
            [1/3, 1/3, 1/3],
            [1/9, 7/9, 1/9],
            [0, 2/3, 1/3],
            [1/3, 2/3, 0],
            [1/9, 4/9, 4/9],
            [0, 1, 0],
            [4/9, 4/9, 1/9],
            [4/9, 1/9, 4/9],
            [0, 1/3, 2/3],        
            [1/9, 1/9, 7/9],
            [0, 0, 1],
            [1/3, 0, 2/3],
            [2/3, 1/3, 0],
            [7/9, 1/9, 1/9],
            [2/3, 0, 1/3],
            [1, 0, 0]
            ])
        )
    POSITION = [2.5, 2.5, 3]
    NORMAL = [0, 0, -1]
    MLAMBERT = 1
    WAVELENGTHS = [620, 530, 475]
    FWHM = [20, 45, 20]
    CONSTELLATION = 'ieee16'
    LUMINOUS_FLUX = 5000

    ILER_REF = np.array(
        [[3.8001e-03, 0.0000e+00, 0.0000e+00],
         [0.0000e+00, 1.9315e-03, 0.0000e+00],
         [0.0000e+00, 0.0000e+00, 1.1960e-02]],
        dtype=np.float32
        )

    AVG_POWER_COLOR = np.array(
        [6.3336e+00, 3.2192e+00, 1.9934e+01],
        dtype=np.float32
        )

    transmitter = Transmitter(
        "Led1",
        position=POSITION,
        normal=NORMAL,
        mlambert=MLAMBERT,
        wavelengths=WAVELENGTHS,
        fwhm=FWHM,
        constellation=CONSTELLATION,
        luminous_flux=LUMINOUS_FLUX
                )        
    
    SPD_REF = np.load('SPD_REF.npy')
    
    print(transmitter)
   
    def test_position(self):
        assert np.array_equal(self.transmitter.position, np.array(self.POSITION))

    def test_normal(self):
        assert np.array_equal(self.transmitter.normal, np.array([self.NORMAL]))

    def test_mlambert(self):
        assert self.transmitter.mlambert == self.MLAMBERT

    def test_wavelengths(self):
        assert np.array_equal(self.transmitter.wavelengths, np.array(self.WAVELENGTHS))

    def test_fwhm(self):
        assert np.array_equal(self.transmitter.fwhm, np.array(self.FWHM))

    def test_constellation(self):
        assert np.allclose(
            self.transmitter.constellation,
            self.SYMBOLS_CONSTELLATION,
            rtol=1e-5
        )
    def test_luminous_flux(self):
        assert self.transmitter.luminous_flux == self.LUMINOUS_FLUX
    
    def test_iler(self):
        assert np.allclose(
            self.transmitter._iler_matrix, 
            self.ILER_REF,
            rtol=1e-4
            )

    def test_avg_power(self):
        assert np.allclose(
            self.transmitter._avg_power, 
            self.AVG_POWER_COLOR,
            rtol=1e-5
            )
    
    def test_led_spd(self):
        assert np.allclose(
            self.SPD_REF,
            self.transmitter._spd_normalized
        )
        
    def test_position_error(self):          
        position_errors = [['a', 2, 3], [2.5, 2.5, 3, 4], 'a']
        
        for options in position_errors:
            with pytest.raises(ValueError):
                transmitter = Transmitter(
                    "Led1",
                    position=options,
                    normal=self.NORMAL,
                    mlambert=self.MLAMBERT,
                    wavelengths=self.WAVELENGTHS,
                    fwhm=self.FWHM,
                    constellation=self.CONSTELLATION,
                    luminous_flux=self.LUMINOUS_FLUX
                            )        
    
    def test_normal_error(self):
        normal_errors = [['a', 2, 3], [2.5, 2.5, 3, 4], 'a']

        for options in normal_errors:
            with pytest.raises(ValueError):
                transmitter = Transmitter(
                    "Led1",
                    position=self.POSITION,
                    normal=options,
                    mlambert=self.MLAMBERT,
                    wavelengths=self.WAVELENGTHS,
                    fwhm=self.FWHM,
                    constellation=self.CONSTELLATION,
                    luminous_flux=self.LUMINOUS_FLUX
                            )
        
    def test_mlambert_error(self):        
        mlambert_erros = ['a', -1, [1, 1]]
        
        for options in mlambert_erros:
            with pytest.raises(ValueError):
                transmitter = Transmitter(
                    "Led1",
                    position=self.POSITION,
                    normal=self.NORMAL,
                    mlambert=options,
                    wavelengths=self.WAVELENGTHS,
                    fwhm=self.FWHM,
                    constellation=self.CONSTELLATION,
                    luminous_flux=self.LUMINOUS_FLUX
                            )            
    
    def test_wavelengths_error(self):
        wavalengths_errors = [[-400, 500, 600], ['a', 2, 3], [400, 500, 600, 700], 'a'] 
        
        for options in wavalengths_errors:
            with pytest.raises(ValueError):
                transmitter = Transmitter(
                    "Led1",
                    position=self.POSITION,
                    normal=self.NORMAL,
                    mlambert=self.MLAMBERT,
                    wavelengths=options,
                    fwhm=self.FWHM,
                    constellation=self.CONSTELLATION,
                    luminous_flux=self.LUMINOUS_FLUX
                            )
                    
    def test_fwhm_error(self):   

        fwdm_errors = [[-10, 50, 60], ['a', 2, 3], [40, 50, 60, 70], 'a'] 
        
        for options in fwdm_errors:
            with pytest.raises(ValueError):
                transmitter = Transmitter(
                    "Led1",
                    position=self.POSITION,
                    normal=self.NORMAL,
                    mlambert=self.MLAMBERT,
                    wavelengths=self.WAVELENGTHS,
                    fwhm=options,
                    constellation=self.CONSTELLATION,
                    luminous_flux=self.LUMINOUS_FLUX
                            )
    
    def test_constellation_error(self):
        constellation_erorrs = ['ook', 'csk', 'ieee', 10, [10, 10]]
        
        for options in constellation_erorrs: 
            with pytest.raises(ValueError):
                transmitter = Transmitter(
                    "Led1",
                    position=self.POSITION,
                    normal=self.NORMAL,
                    mlambert=self.MLAMBERT,
                    wavelengths=self.WAVELENGTHS,
                    fwhm=self.FWHM,
                    constellation=options,
                    luminous_flux=self.LUMINOUS_FLUX
                            )
        
    def test_luminous_flux_error(self):
        flux_errors = [-100, 0, 'a', 'wrong']

        for options in flux_errors:
            with pytest.raises(ValueError):
                transmitter = Transmitter(
                    "Led1",
                    position=self.POSITION,
                    normal=self.NORMAL,
                    mlambert=self.MLAMBERT,
                    wavelengths=self.WAVELENGTHS,
                    fwhm=self.FWHM,
                    constellation=self.CONSTELLATION,
                    luminous_flux=options
                            )
