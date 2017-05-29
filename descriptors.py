#!/usr/bin/python3

# SIFT/SURF only works in opencv_contrib as it is a patented algorithm and thus
# has been moved out of the base install of the opencv package.
# easiest way is to install with pip:
#
# $ pip3 install opencv-contrib-python
#

import  os
import  sys
import  cv2
import  pickle
import  numpy               as      np
import  matplotlib.pyplot   as      plt

# (module global instantiation of extractor objects
#  to reduce overhead in functions)

# DETECTORS
# FAST feature detector (used for different descriptors)
__fast  = cv2.FastFeatureDetector_create()
# MSER Maximally Stable Extremal Regions detector
__mser  = cv2.MSER_create()
# DESCRIPTORS (and sometimes detectors)
# SIFT/SURF detector and descriptors
# SIFT: Lapl. of Gauss.  is approx. with the Diff. of Gauss.
# SURF: Lapl. of Gauss.  is approx. with a box filter (faster).
__sift  = cv2.xfeatures2d.SIFT_create()
__surf  = cv2.xfeatures2d.SURF_create(extended=True)
# BRISK Binary Robust Invariant Scalable Keypoints
__brisk = cv2.BRISK_create()
# KAZE features and descriptors
__kaze  = cv2.KAZE_create()
# BRIEF descriptor extractor
__brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
# ORB detector & descriptors
__orb   = cv2.ORB_create()
# HoG descriptor extractor as CHoG is not available in openCV due to copyright
winSize             = (64,64)
blockSize           = (32, 32) # default is (16,16)
blockStride         = (16, 16) # default is (8,8)
cellSize            = (8,8)
nbins               = 9
derivAperture       = 1
winSigma            = 4.
histogramNormType   = 0
L2HysThreshold      = 2.0000000000000001e-01
gammaCorrection     = 0
nlevels             = 4 # default is 64
__hog   = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,
                            nbins,derivAperture,winSigma,
                            histogramNormType,L2HysThreshold,
                            gammaCorrection,nlevels)


def __show_keypoints(gray,kp,img):
    img = cv2.drawKeypoints(gray,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    plt.figure()
    plt.imshow(img)
    plt.show()


def extract_SIFT(imgfile, opt=None):
    """
    Takes a filename as input and returns a pair of keypoints and descriptors.
    Feature Detector:       SIFT
    Descriptor Extractor:   SIFT
    options:
    opt = 'show_keypoints' shows a grayscale version
    of the image with all found keypoints highlighted
    and to scale w.r.t. size of descriptor
    """
    gray     = cv2.imread(imgfile, 0)
    kp, des = __sift.detectAndCompute(gray,None)
    if opt == 'show_keypoints':
        __show_keypoints(gray,kp,img)

    return des


def extract_SURF(imgfile, opt=None):
    """
    Takes a filename as input and returns a pair of keypoints and descriptors.
    Feature Detector:       SURF
    Descriptor Extractor:   SURF
    Options:
    opt = 'show_keypoints' shows a grayscale version
    of the image with all found keypoints highlighted
    and to scale w.r.t. size of descriptor
    """
    img     = cv2.imread(imgfile)
    gray    = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kp, des = __surf.detectAndCompute(gray,None)
    if opt == 'show_keypoints':
        __show_keypoints(gray,kp,img)

    return des


def extract_BRIEF(imgfile, opt=None):
    """
    Takes a filename as input and returns a pair of keypoints and descriptors.
    Feature Detector:       FAST
    Descriptor Extractor:   BRIEF
    Options:
    opt = 'show_keypoints' shows a grayscale version
    of the image with all found keypoints highlighted
    and to scale w.r.t. size of descriptor
    """
    img     = cv2.imread(imgfile)
    gray    = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kp      = __fast.detect(gray,None)
    kp, des = __brief.compute(gray, kp)
    if opt == 'show_keypoints':
        __show_keypoints(gray,kp,img)

    return des


def extract_ORB(imgfile, opt=None):
    """
    # ORB - ORiented BRIEF (FAST+BRIEF with enhancements)
    Takes a filename as input and returns a pair of keypoints and descriptors.
    Feature Detector:       ORB (FAST)
    Descriptor Extractor:   ORB (BRIEF)
    Options:
    opt = 'show_keypoints' shows a grayscale version
    of the image with all found keypoints highlighted
    and to scale w.r.t. size of descriptor
    """
    img     = cv2.imread(imgfile)
    gray    = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kp, des = __orb.detectAndCompute(gray, None)
    if opt == 'show_keypoints':
        __show_keypoints(gray,kp,img)

    return des


def extract_HOG(imgfile):
    """
    Histogram of Oriented Gradients as CHOG is not available in openCV due to copyright
    Takes a filename as input and returns a descriptor.
    Feature Detector:       None - HOG is a global descriptor
    Descriptor Extractor:   HOG
    """
    winStride = (32,32)
    padding = (32,32)
    gray = cv2.cvtColor(cv2.imread(imgfile),cv2.COLOR_BGR2GRAY)
    des  = __hog.compute(gray, winStride, padding)
    return des


def extract_BRISK(imgfile, opt=None):
    """
    # BRISK Binary Robust Invariant Scalable Keypoints
    Takes a filename as input and returns a pair of keypoints and descriptors.
    Feature Detector:       BRISK
    Descriptor Extractor:   BRISK
    Options:
    opt = 'show_keypoints' shows a grayscale version
    of the image with all found keypoints highlighted
    and to scale w.r.t. size of descriptor
    """
    img     = cv2.imread(imgfile)
    gray    = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kp, des = __brisk.detectAndCompute(gray, None)
    if opt == 'show_keypoints':
        __show_keypoints(gray,kp,img)

    return des

def extract_KAZE(imgfile, opt=None):
    """
    # KAZE Nonlinear scale space with diffusion filtering to prevent feature blur
    Takes a filename as input and returns a pair of keypoints and descriptors.
    Feature Detector:       KAZE
    Descriptor Extractor:   KAZE
    Options:
    opt = 'show_keypoints' shows a grayscale version
    of the image with all found keypoints highlighted
    and to scale w.r.t. size of descriptor
    """
    img     = cv2.imread(imgfile)
    gray    = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kp, des = __kaze.detectAndCompute(gray, None)
    if opt == 'show_keypoints':
        __show_keypoints(gray,kp,img)

    return des




if __name__ == "__main__":
    #Walk over data directory containing the source images in a
    #subdirectory according to their class
    #./data
      #/set1/
        #'---> class1/
            #'---> img1.png
            #'---> img2.png
        #'---> class2/
            #'---> img1.png ...
    methods = ['sift', 'surf', 'brief', 'orb', 'hog', 'brisk', 'kaze']

    dispatch = {
        "sift":     extract_SIFT,
        "surf":     extract_SURF,
        "brief":    extract_BRIEF,
        "orb":      extract_ORB,
        "hog":      extract_HOG,
        "brisk":    extract_BRISK,
        "kaze":     extract_KAZE
    }
    # root directory of the datasets
    rootdir = sys.argv[1]
    # if no descriptor name was given, default to all
    if len(sys.argv) < 3:
        descriptors = methods
    else:
        descriptors = sys.argv[2].split(sep=',')

    #print("Selected descriptor methods: \n  {}".format(descriptors))

    for subdir, dirs, files in os.walk(rootdir):
        #print(subdir)
        for file in files:
            if file.endswith(".bmp"):
                imagefile = os.path.join(subdir, file)
                for method in descriptors:
                    des = dispatch[method](imagefile)
                    pickle.dump(des, open(imagefile + '.' + method, 'wb'))

#EOF
