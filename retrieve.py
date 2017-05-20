import  cv2
import  sys
import  os
import  glob
import  pickle
import  numpy as np

def rocPoints(boolData):
    totalPos = sum(1 for d in boolData if d == True)
    totalNeg = sum(1 for d in boolData if d == False)
    if totalPos < 1 or totalNeg < 1:
        raise ValueError("must contain at least one positive and negative result")
    rocPoints = []
    for i in range(len(boolData) + 1):
        dataPart = boolData[:i]
        partPos = sum(1 for d in dataPart if d == True)
        partNeg = sum(1 for d in dataPart if d == False)
        falsePosRate = partNeg / float(totalNeg)
        truePosRate = partPos / float(totalPos)
        rocPoints.append((falsePosRate, truePosRate))
    rocPoints = sorted(rocPoints)
    # for all points at a given x, keep only that with the highest y
    rocPoints = [rocPoints[i] for i in range(len(rocPoints))
            if i == len(rocPoints) - 1 or rocPoints[i][0] < rocPoints[i + 1][0]]
    return rocPoints

def rocAreaBool(boolData):
    points = rocPoints(boolData)
    area = 0.0
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        area += (p2[0] - p1[0]) * p1[1]
    return area

def rocAreaFromResults(queryDescriptorFilename, results):
    queryCategory = descriptorNameCategory(queryDescriptorFilename)[1]
    boolData = []
    for result in results:
        resultCategory = descriptorNameCategory(result[1])[1]
        boolData.append(resultCategory == queryCategory)
    return rocAreaBool(boolData)

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

def fromSamePicture(descriptorFileA, descriptorFileB):
    return descriptorFileA.split("/")[-1] == descriptorFileB.split("/")[-1]

def printResults(queryDescriptorFilename, results):
    queryName, queryCategory = descriptorNameCategory(queryDescriptorFilename)
    rocArea = rocAreaFromResults(queryDescriptorFilename, results)
    print("query={} category={} rocArea={}".format(queryName, queryCategory, rocArea))
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
    queryDir            = sys.argv[1]
    trainDir            = sys.argv[2]
    descriptorType      = sys.argv[3]
    bf                  = createMatcher(descriptorType)
    queryDescriptors    = getDescriptors(queryDir, descriptorType)
    trainDescriptors    = getDescriptors(trainDir, descriptorType)

    rocAreas = []
    for queryDesFile, queryDes in queryDescriptors:
        results = []

        for trainDesFile, trainDes in [d for d in trainDescriptors if not fromSamePicture(d[0], queryDesFile)]:

            trainDesDist = doMatching(queryDes, trainDes, bf)
            results.append((trainDesDist, trainDesFile))

        rocAreas.append(rocAreaFromResults(queryDesFile, sorted(results)))
        printResults(queryDesFile, sorted(results))
    print("query: {} train: {} descriptor: {} avgRoc: {}".format(queryDir, trainDir, descriptorType, str(np.average(rocAreas))))
