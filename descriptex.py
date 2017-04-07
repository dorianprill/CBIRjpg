#!/usr/bin/python

"""
file name:  descriptex.py
info:       Module with a collection of image descriptor extraction
            functions such as: SIFT/SURF, CHoG, HIP, ....

"""

import  sys

import  numpy           as np
import  scipy           as sp
import  scipy.signal    as signal
import  scipy.ndimage   as ndimage

from    math            import *
from    cv2             import *
from    PIL             import Image


# TODO
# add functions that take the image path as argument and return a
# pandas.Series/pandas.DataFrame including path/name/class and descript.



