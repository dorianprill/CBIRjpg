import  os
from    descriptex import *

#Walk over data directory containing the source images in a
#subdirectory according to their class
#./data
  #'---> class1/
      #'---> img1.png
      #'---> img2.png
  #'---> class2/
      #'---> img1.png ...

# root directory of the dataset
rootdir = './data'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print(os.path.join(subdir, file))
        # TODO:
        # 1. compress images with jpg/200/XR
        # 2. extract features from images and save them as pandas
        #    DataFrame with their path/name/class for easy eval

# cross validation for query
# calculate query rank and dump results as own dataframe

#EOF
