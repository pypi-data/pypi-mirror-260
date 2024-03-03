# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT 
# WITH UNLIMITED RIGHTS
#
# Grant No.: 80NSSC21K0651
# Grantee Name: Universities Space Research Association
# Grantee Address: 425 3rd Street SW, Suite 950, Washington DC 20024
#
# Developed by: Colleen A. Wilson-Hodge
# 			    National Aeronautics and Space Administration (NASA)
#     			Marshall Space Flight Center
#     			Astrophysics Branch (ST-12)
#
# This work is a derivative of the Gamma-ray Data Tools (GDT), including the 
# Core and Fermi packages, originally developed by the following:
#
#     William Cleveland and Adam Goldstein
#     Universities Space Research Association
#     Science and Technology Institute
#     https://sti.usra.edu
#     
#     Daniel Kocevski
#     National Aeronautics and Space Administration (NASA)
#     Marshall Space Flight Center
#     Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not 
# use this file except in compliance with the License. You may obtain a copy of 
# the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
# License for the specific language governing permissions and limitations under 
# the License.
#
#Make Phaii for RXTE ASM data
from gdt.core.data_primitives import Ebounds, Gti, TimeEnergyBins
from gdt.core.phaii import Phaii
from astropy.io import ascii
import astropy.io.fits as fits
import numpy as np
import os
from gdt.core import data_path
asm_path = data_path/'rxte-asm'

__all__ = ['RxtePhaiiNoHeaders']

class RxtePhaiiNoHeaders(Phaii):
    """Class for RXTE ASM PHAII data
    """
    def __init__(self, *args):            
        super(RxtePhaiiNoHeaders, self).__init__(*args)
        self._detector = None
        
    @property
    def detector(self):
        """(str): The detector (ssc1, ssc2, or ssc3)
        """
        return self._detector
    
    @classmethod
    def open_ascii(cls, dwell_filename, detector, t0):
        """Open the ASCII version of the PHAII data.
        
        Args:
            dwell_filename (str): The dwell filename
            detector (str): The ASM detector (ssc1, ssc2, or ssc3)
            t0 (float): The MET trigger time.
        
        Returns:
            (:class:`RxtePhaiiNoHeaders`)
        """
        ascii_filename = os.path.join(asm_path,dwell_filename)       			   			  	  
        obj = cls()
        #check if ascii_filename exists	
        if os.path.isfile(ascii_filename):
            #if the filename exists then open it
            obj._filename = ascii_filename

            #open and read the text table of ASM dwell information
            data = ascii.read(ascii_filename)
            #rename colimns
	        #first column is spacecraft time (MET-3.37s)
            data["col1"].name="sct"
            #second column is count rate in 1.5-3 keV band for ssc0
            data["col2"].name="ssc1a"
            #third column is count rate in 3-5 keV band for ssc0
            data["col3"].name="ssc1b"
            #fourth column is count rate in 5-12 keV band for ssc0
	        # pattern repeats with columns 5-7 corresponding to the three bands in ssc1 and 8-10 for the three bands in ssc2
            data["col4"].name="ssc1c"
            data["col5"].name="ssc2a"
            data["col6"].name="ssc2b"
            data["col7"].name="ssc2c"
            data["col8"].name="ssc3a"
            data["col9"].name="ssc3b"
            data["col10"].name="ssc3c"
            # RXTE ASM has fixed energy bounds 1.5-3, 3-5, 5-12 keV for all three detectors.
            emin = np.array([1.5,3.0,5.0])
            emax = np.array([3.0,5.0,12.0])
            obj._ebounds = Ebounds.from_bounds(emin, emax)
            # arrange RXTE ASM data into TimeEnergyBins inputs
            if detector == "ssc1":
                counts = np.transpose(np.array([data["ssc1a"],data["ssc1b"],data["ssc1c"]]))
            elif detector == "ssc2":
                counts = np.transpose(np.array([data["ssc2a"],data["ssc2b"],data["ssc2c"]]))
            elif detector == "ssc3":
                counts = np.transpose(np.array([data["ssc3a"],data["ssc3b"],data["ssc3c"]]))
            else:
                #check if detector input correctly
                print (detector,' not found. Input ssc1, ssc2, or ssc3')
                return
            #define times in MET with 1 second long bins
            tstart = np.array([data["sct"]])+3.37843167-t0
            tstop = np.array([data["sct"]])+4.37843167-t0
            #exposure time is not given in data files. Assume 1 second duration.
            exposure = np.ones(np.size(tstart))
            #put TimeEnergyBins into Phaii class 			
            obj._data = TimeEnergyBins(counts, tstart, tstop, exposure, emin, emax)
            # Set GTI as duration of data
            # obj._gti = Gti.from_bounds(gti_start, gti_end)
            obj._gti = Gti.from_bounds(np.amin(tstart),np.amax(tstop))
            # set _detector to input detector value
            obj._detector = detector
            obj._trigtime = t0
            return obj
        else:
            #Error handling - inform user that file is not found and return nothing.
            print (ascii_filename,' not found.')
            return
	    
    def _build_hdulist(self):

        #create FITS and primary header
        hdulist = fits.HDUList()
        primary_hdu = fits.PrimaryHDU()
        hdulist.append(primary_hdu)
        
        #create the ebounds extension
        ebounds_hdu = self._ebounds_table()
        hdulist.append(ebounds_hdu)
        
        #create the spectrum extension
        spectrum_hdu = self._spectrum_table()
        hdulist.append(spectrum_hdu)        
        
        #create the GTI extension
        gti_hdu = self._gti_table()
        hdulist.append(gti_hdu)
        
        return hdulist
            
    def _ebounds_table(self):
        chan_col = fits.Column(name='CHANNEL', format='1I', 
                               array=np.arange(self.num_chans, dtype=int))
        emin_col = fits.Column(name='E_MIN', format='1E', unit='keV', 
                               array=self.ebounds.low_edges())
        emax_col = fits.Column(name='E_MAX', format='1E', unit='keV', 
                               array=self.ebounds.high_edges())
        
        hdu = fits.BinTableHDU.from_columns([chan_col, emin_col, emax_col])

        return hdu

    def _spectrum_table(self):
        tstart = np.copy(self.data.tstart)
        tstop = np.copy(self.data.tstop)
        if self.trigtime is not None:
            tstart += self.trigtime
            tstop += self.trigtime
        
        counts_col = fits.Column(name='COUNTS', 
                                 format='{}I'.format(self.num_chans), 
                                 bzero=32768, bscale=1, unit='count',
                                 array=self.data.counts)
        expos_col = fits.Column(name='EXPOSURE', format='1E', unit='s', 
                                array=self.data.exposure)
        time_col = fits.Column(name='TIME', format='1D', unit='s', 
                               bzero=self.trigtime, array=tstart)
        endtime_col = fits.Column(name='ENDTIME', format='1D', unit='s', 
                                  bzero=self.trigtime, array=tstop)
        hdu = fits.BinTableHDU.from_columns([counts_col, expos_col, 
                                             time_col, endtime_col])

        return hdu

    def _gti_table(self):
        tstart = np.array(self.gti.low_edges())
        tstop = np.array(self.gti.high_edges())

        start_col = fits.Column(name='START', format='1D', unit='s', 
                                bzero=self.trigtime, array=tstart)
        stop_col = fits.Column(name='STOP', format='1D', unit='s', 
                                bzero=self.trigtime, array=tstop)
        hdu = fits.BinTableHDU.from_columns([start_col, stop_col])
        
        return hdu

    @classmethod
    def open_fits(cls, fits_filename, detector=None, t0=0.0, **kwargs):
        """Open the FITS version of the PHAII data created by gdt-rxte.
        
        Args:
            fits_filename (str): Name of the file
            detector (str, optional): The detector
            t0 (float, optional): The trigger time. Default is 0.0
        """
        obj = super().open(fits_filename, **kwargs)
        #check if filename exists	
        if os.path.isfile(fits_filename):
            #if the filename exisits then open it
            obj._filename = fits_filename
       
            # the channel energy bounds
            ebounds = Ebounds.from_bounds(obj.column(1, 'E_MIN'), obj.column(1, 'E_MAX'))
            # the 2D time-channel counts data
            time = obj.column(2, 'TIME')
            endtime = obj.column(2, 'ENDTIME')
            
            exposure = obj._assert_exposure(obj.column(2, 'EXPOSURE'))
            
            data = TimeEnergyBins(obj.column(2, 'COUNTS'), time-t0, endtime-t0, exposure, obj.column(1, 'E_MIN'), obj.column(1, 'E_MAX'))

            # the good time intervals
            gti_start = obj.column(3, 'START')
            gti_stop = obj.column(3, 'STOP')
            gti = Gti.from_bounds(gti_start, gti_stop)
            cls.detector=detector
            class_ = cls
            obj.close()
            return class_.from_data(data, gti=gti, trigger_time=t0, filename=obj.filename)
        else:
            #Error handling - inform user that file is not found and return nothing.
            print (fits_filename,' not found.')
            return
