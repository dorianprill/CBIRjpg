
# CBIR JPEG Study

Comparative study on Content-Based Image Retrieval from compressed images using different compression algorithms and content concepts. Compression: (jpeg, jpeg2000, jpegXR) Content: (SIFT, ...).
To avoid artifacts from subsequent compression, an uncompressed dataset is used.


# How it Works
You basically just have to run 'python doEverything.py 1 1 1'. Sit back and enjoy the show!

# Requirements

You will need at least Python 3 with [opencv](http://www.opencv.org/) and numpy/scipy.
Preferably, use the pip package manager to install these libraries.
As some of the algorithms (such as SIFT/SURF) are considered non-free, they have
been moved out of the base install of opencv and are only available in the
 [opencv-contrib package](https://pypi.python.org/pypi/opencv-contrib-python/3.2.0.7).  
Luckily, there's package availabe to install with pip: opencv-contrib-python

## Dataset

After you have installed the required software you will also need the following data sets:

[INRIA Holidays Dataset](http://lear.inrialpes.fr/~jegou/data.php#holidays)


Extract all datasets to analyze to a subfolder named `data` so that your direcotry structure resembles this: `cbir/data/dataset1/class1/lotsoffiles.jpg`.


# About the authors

This study was carried out by a group of students from the University of Salzburg under supervision of ...

[profile of X](https://www.google.com).
