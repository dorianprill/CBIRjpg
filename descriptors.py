#!/usr/bin/python
# tested with python3.6

# SIFT/SURF only works in opencv_contrib as it is a patented algorithm and thus
# has been moved out of the base install of the opencv package.
# easiest way is to install with pip:
#
# $ pip3.6 install opencv-contrib-python
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
__surf  = cv2.xfeatures2d.SURF_create()
# BRISK Binary Robust Invariant Scalable Keypoints
__brisk = cv2.BRISK_create()
# KAZE features and descriptors
__kaze  = cv2.KAZE_create()
# BRIEF descriptor extractor
__brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
# ORB detector & descriptors
__orb   = cv2.ORB_create()



# HoG descriptor extractor as CHoG is not available in openCV due to copyright
__hog   = cv2.HOGDescriptor()

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
    img     = cv2.imread(imgfile)
    gray    = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kp, des = __sift.detectAndCompute(gray,None)
    if opt == 'show_keypoints':
        __show_keypoints(gray,kp,img)

    return kp,des


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

    return kp,des


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

    return kp,des


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

    return kp,des


def extract_HOG(imgfile):
    """
    Histogram of Oriented Gradients as CHOG is not available in openCV due to copyright
    Takes a filename as input and returns a descriptor.
    Feature Detector:       None - HOG is a global descriptor
    Descriptor Extractor:   HOG
    """
    gray = cv2.cvtColor(cv2.imread(imgfile),cv2.COLOR_BGR2GRAY)
    des  = __hog.compute(gray)
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

    return kp,des

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

    return kp,des




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

    # root directory of the datasets
    rootdir = sys.argv[1]
    descriptor = sys.argv[2]

    for subdir, dirs, files in os.walk(rootdir):
        print(subdir)
        for file in files:
            if file.endswith((".dng", ".jpg", "jp2", "jxr")):
                imagefile = os.path.join(subdir, file)
                print("  {}".format(file))
                if descriptor == 'sift' or descriptor == "all" :
                    kp, des = extract_SIFT(imagefile)
                    pickle.dump(des, open(imagefile + '.sift', 'wb'))
                if descriptor == "surf" or descriptor == "all":
                    kp, des = extract_SURF(imagefile)
                    pickle.dump(des, open(imagefile + '.surf', 'wb'))
                if descriptor == 'brief' or descriptor == "all":
                    kp, des = extract_BRIEF(imagefile)
                    pickle.dump(des, open(imagefile + '.brief', 'wb'))
                if descriptor == 'hog' or descriptor == "all": 
                    des     = extract_HOG(imagefile)
                    # BEWARE: the generated files can be huge (several gigabytes)
                    # pickle.dump(des, open(imagefile + '.hog', 'wb'))
                if descriptor == 'brisk' or descriptor == "all":
                    kp, des = extract_BRISK(imagefile)
                    pickle.dump(des, open(imagefile + '.brisk', 'wb'))
                if descriptor == 'kaze' or descriptor == "all":
                    kp, des = extract_KAZE(imagefile)
                    pickle.dump(des, open(imagefile + '.kaze', 'wb'))
                if descriptor == 'orb' or descriptor == "all":
                    kp, des = extract_ORB(imagefile)
                    pickle.dump(des, open(imagefile + '.orb', 'wb'))

#EOF
