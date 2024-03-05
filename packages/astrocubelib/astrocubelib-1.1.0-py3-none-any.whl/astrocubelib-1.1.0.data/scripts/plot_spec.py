#!python
import sys
from pyraf import iraf

namespec=sys.argv[1]

print ('plotting ', namespec)

iraf.noao()
iraf.onedspec(_doprint=0)
iraf.splot(namespec)
