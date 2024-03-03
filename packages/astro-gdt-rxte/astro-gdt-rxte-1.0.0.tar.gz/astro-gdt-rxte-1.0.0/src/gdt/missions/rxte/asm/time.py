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
from astropy.time import TimeFromEpoch, TimeUnique, ScaleValueError, Time

__all__ = ['RxteSecTime', 'Time']

class RxteSecTime(TimeFromEpoch):
    """Represents the number of seconds elapsed since Jan 1, 1994 00:00:00 UTC including leap seconds and RXTE clock correction of 3.37843167E+00 s """
    
    name = 'rxte'
    """(str): Name of the mision"""    
    
    unit = 1.0/86400
    """(float): unit in days"""
    
    epoch_val = '1994-01-01 00:01:03.56243157'
    """(str): The epoch in Terrestrial Time"""
    
    epoch_val2 = None
    
    epoch_scale = 'tt' # Terrestrial Time
    """(str): The scale of :attr: `epoch_val`"""
    
    epoch_format = 'iso'
    """(str): Format of :attr:`epoch_val`"""
    
from astropy.time import Time as AstropyTime

class Time(AstropyTime):    

    @property
    def rxte_sct(self):
        """(float): RXTE spacecraft time (used for dwell file names) 
        corresponding to the MET"""
        return self.rxte - 3.37843167
	
    @property
    def rxte_mission_day(self):
        """(float): RXTE mission day - this needs to be in Spacecraft time to 
        match the dwell sequence"""
        return int((self.rxte_sct)/86400)
    
    @property
    def rxte_mission_week(self):
        """(float): RXTE mission week - this is computed in MJD based on the 
        short term short form timelines available through the RXTE GOF. 
        Mission week 0 started on 1996-Jan-26"""
        return int((self.mjd-50108.0)/7)
	    
 
