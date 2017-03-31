
# CBIR JPEG Study

Comparative study on Content-Based Image Retrieval from compressed images using different compression algorithms and content concepts. Compression: (jpeg, jpeg2000, jpegXR) Content: (SIFT, ...).
To produce comparable results, standard datasets used in various image retrieval related work are used for this study.


# How it works

1. Features are extracted from the images with several methods
2. The images are then compressed using several jpeg standard algorithms
3. An (uncompressed?) image is used to query the database


# Requirements

You will need at least Python 3 with [opencv](http://www.opencv.org/), numpy/scipy, pandas, ggplot2.
Preferably, use the pip package manager to install these libraries.

## Dataset

After you have installed the required software you will also need the following data sets:

[INRIA Holidays Dataset](http://lear.inrialpes.fr/~jegou/data.php#holidays)


Extract all datasets to analyze to a subfolder named `data` (i.e. `cbir/data/dataset1/lotsoffiles.jpg`).


# About the authors

This study was carried out by a group of students from the University of Salzburg.

[profile of X](https://www.google.com).
