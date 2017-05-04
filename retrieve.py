import  cv2
import  sys
import  os
import  glob
import  pickle
import  numpy as np

def createMatcher(descriptor):
    if descriptor == 'sift' or descriptor == 'surf' or descriptor == 'kaze':
        bf = cv2.BFMatcher()
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)

    else:
        bf = cv2.BFMatcher(normType=cv2.NORM_HAMMING)
        FLANN_INDEX_LSH = 6
        index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2

    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    
    return bf

def descriptorNameCategory(descriptorFilename):
    dSplit = descriptorFilename.split("/")
    return (dSplit[-1], dSplit[-2])

def printResults(queryDescriptorFilename, results):
    queryName, queryCategory = descriptorNameCategory(queryDescriptorFilename)
    print("query={} category={}".format(queryName, queryCategory))
    results = sorted(results)
    for result in results:
        trainName, trainCategory = descriptorNameCategory(result[1])
        print("train={} category={} distance={}".format(trainName, trainCategory, result[0]))

def getDescriptors(directory, descriptorType):
    descriptorFilenames = glob.glob(os.path.join(directory, "*/*." + descriptorType))
    return sorted((name, loadDescriptor(name)) for name in descriptorFilenames)

def loadDescriptor(descriptorFile):
    return pickle.load(open(descriptorFile, 'rb'))

def doMatching(queryDescriptor, trainDescriptor, matcher):
    minRatio = 0.9
    matches = bf.knnMatch(queryDescriptor, trainDescriptor, k = 2)
    goodMatches = [m for m, n in matches if m.distance < minRatio * n.distance]
    if len(goodMatches) == 0:
        raise ValueError("no matches survived ratio test")
    return np.average([m.distance for m in goodMatches])


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
    queryDir = sys.argv[1]
    trainDir = sys.argv[2]
    descriptorType = sys.argv[3]

    bf = createMatcher(descriptorType)
    queryDescriptors = getDescriptors(queryDir, descriptorType)
    trainDescriptors = getDescriptors(trainDir, descriptorType)

    for queryDesFile, queryDes in queryDescriptors:       
        results = []
        
        for trainDesFile, trainDes in trainDescriptors:
        
            trainDesDist = doMatching(queryDes, trainDes, bf)
            results.append((trainDesDist, trainDesFile))

        printResults(queryDesFile, results)
        print("")
