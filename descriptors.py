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
import  numpy               as      np
import  matplotlib.pyplot   as      plt

def get_sift_descriptors(imgfile, opt=None):
    """
    Takes a filename as input and returns a pair of
    SIFT keypoints and descriptors
    options:
    opt = 'show_keypoints' shows a grayscale version
    of the image with all found keypoints highlighted
    and to scale w.r.t. size of descriptor
    """
    img     = cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)
    gray    = img
    sift    = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(gray,None)
    if opt == 'show_keypoints':
        img = cv2.drawKeypoints(gray,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        plt.figure()
        plt.imshow(img)
        plt.show()

    return kp,des


if __name__ == "__main__":
    #Walk over data directory containing the source images in a
    #subdirectory according to their class
    #./data
        #'---> class1/
            #'---> img1.png
            #'---> img2.png
        #'---> class2/
            #'---> img1.png ...
    # root directory of the datasets
    rootdir = './data/test/500/'
    dataset = []
    
    queryKp, queryDes = get_sift_descriptors(sys.argv[1])
    queryType = sys.argv[1].split('/')[-2]
    print(queryType)

    bf = cv2.BFMatcher()
    goodMatches = []
    results = []
    imagesToRetrieve = 3

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            # find the keypoints and compute descriptors
            kp, des = get_sift_descriptors(os.path.join(subdir, file))
            matches = bf.knnMatch(queryDes, des, k=2)
            for m,n in matches:
                if m.distance < 0.75*n.distance:
                    goodMatches.append(m)

            distances = list(map(lambda m: m.distance, goodMatches))
            results.append((np.average(distances), subdir.split('/')[-1]))

            # TODO: add to ... dataframe? panel?

    correctImages = len(list(filter(lambda r: r[1] == queryType , sorted(results)[:3])))

    print("total: " + str(imagesToRetrieve) + " found: " + str(correctImages))

    print(sorted(results))

#EOF
