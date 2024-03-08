'''
pyatmos package

This package is an archive of scientific routines that implement the 
estimation of atmospheric properties for various atmospheric models, such
as exponential, coesa76, nrlmsise00, and jb2008. 

'''    

from .standardatmos.expo import expo
from .standardatmos.coesa76 import coesa76

from .msise.spaceweather import download_sw_nrlmsise00,read_sw_nrlmsise00
from .jb2008.spaceweather import download_sw_jb2008,read_sw_jb2008

from .msise.nrlmsise00 import nrlmsise00
from .jb2008.jb2008 import jb2008
from .utils import data_prepare

# Load and update the EOP file and Leap Second file
data_prepare.iers_load() 