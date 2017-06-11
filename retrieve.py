#!/usr/bin/python3

import  cv2
import  sys
import  os
import  glob
import  pickle
import  numpy as np

def createMatcher(descriptorType):
    if descriptorType in ["sift", "surf", "kaze"]:
        return cv2.FlannBasedMatcher({"algorithm" : 1, "trees" : 1}, {"checks" : 2})
    if descriptorType in ["brief"]:
        return cv2.FlannBasedMatcher(dict(algorithm = 6,
                   table_number = 1,
                   key_size = 20,
                   multi_probe_level = 1), {})
    if descriptorType in ["brisk"]:
        return cv2.FlannBasedMatcher(dict(algorithm = 6,
                   table_number = 3,
                   key_size = 20,
                   multi_probe_level = 1), {})
    if descriptorType in ["orb"]:
        return cv2.BFMatcher(cv2.NORM_HAMMING)
    if descriptorType in ["kaze"]:
        return cv2.BFMatcher(cv2.NORM_L2)

def rocPoints(boolData):
    totalPos = sum(1 for d in boolData if d == True)
    totalNeg = sum(1 for d in boolData if d == False)
    if totalPos < 1 or totalNeg < 1:
        raise ValueError("must contain at least one positive and negative result")
    rocPoints = []
    for i in range(len(boolData) + 1):
        dataPart        = boolData[:i]
        partPos         = sum(1 for d in dataPart if d == True)
        partNeg         = sum(1 for d in dataPart if d == False)
        falsePosRate    = partNeg / float(totalNeg)
        truePosRate     = partPos / float(totalPos)
        rocPoints.append((falsePosRate, truePosRate))
    rocPoints = sorted(rocPoints)
    # for all points at a given x, keep only that with the highest y
    rocPoints = [rocPoints[i] for i in range(len(rocPoints))
            if i == len(rocPoints) - 1 or rocPoints[i][0] < rocPoints[i + 1][0]]
    return rocPoints

def rocAreaBool(boolData):
    points  = rocPoints(boolData)
    area    = 0.0
    for i in range(len(points) - 1):
        p1, p2  = points[i], points[i + 1]
        area    += (p2[0] - p1[0]) * p1[1]
    return area

def rocAreaFromResults(queryDescriptorFilename, results):
    queryCategory = descriptorNameCategory(queryDescriptorFilename)[1]
    boolData = []
    for result in results:
        resultCategory = descriptorNameCategory(result[1])[1]
        boolData.append(resultCategory == queryCategory)
    return rocAreaBool(boolData)

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
    if not descriptorFilenames:
        raise Exception("no descriptor files")
    return sorted((name, loadDescriptor(name)) for name in descriptorFilenames)

def loadDescriptor(descriptorFile):
    return pickle.load(open(descriptorFile, 'rb'))

def doMatching(queryDescriptor, trainDescriptor, matcher):
    if queryDescriptor is None or len(queryDescriptor) == 0 or trainDescriptor is None or len(trainDescriptor) == 0:
        print("warning: no descriptor available")
        return 0.0
    #print("matching...")
    matches = matcher.match(queryDescriptor, trainDescriptor)
    return np.average([m.distance for m in matches])

def getClassFromPath(path):
    return path.split("/")[-2:-1]

def getNumberOfRelevantItemsForQuery(query):
    path = os.path.dirname(query)
    relevantItems = len([name for name in os.listdir(path) if os.path.isfile(path + '/' + name) and name.endswith('.bmp')])
    return relevantItems

def calculateFScore(precision, recall, beta=1):
    b2 = beta * beta
    return (1 + b2) * ((precision * recall)/((b2*precision) + recall))

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
    queryDescriptors    = getDescriptors(queryDir, descriptorType)
    trainDescriptors    = getDescriptors(trainDir, descriptorType)
    matcher = createMatcher(descriptorType)

    rocAreas   = []
    f05scores  = []
    f1scores   = []
    f2scores   = []
    for queryDesFile, queryDes in queryDescriptors:
        results = []

        for trainDesFile, trainDes in [d for d in trainDescriptors if not fromSamePicture(d[0], queryDesFile)]:

            trainDesDist = doMatching(queryDes, trainDes, matcher)
            results.append((trainDesDist, trainDesFile))

        rocAreas.append(rocAreaFromResults(queryDesFile, sorted(results)))
        #printResults(queryDesFile, sorted(results))
        #print("-------------------")
        #print(sorted(results)[:5])

        truePositives  = 0
        falsePositives = 0
        relevantItems  = getNumberOfRelevantItemsForQuery(queryDesFile)
        selectedItems  = 5
        queryClass = getClassFromPath(queryDesFile)
        for result in sorted(results)[:selectedItems]:
            resultClass = getClassFromPath(result[1])
            if resultClass == queryClass:
                truePositives  += 1
            else:
                falsePositives += 1 # atm not used but might be useful
        
        precision = truePositives / selectedItems
        recall    = truePositives / relevantItems
        f05scores.append(calculateFScore(precision, recall, 0.5))
        f1scores.append(calculateFScore(precision, recall, 1))
        f2scores.append(calculateFScore(precision, recall, 2))
        
    
    print('f0.5: '+ str(np.average(f05scores)))
    print('f1: ' + str(np.average(f1scores)))
    print('f2: ' + str(np.average(f2scores)))

    print("query:{}"
            "|trainComprMode:{}"
            "|trainComprRatio:{}"
            "|descriptor:{}"
            "|avgRoc:{}".format(queryDir,
                                trainDir.split(sep='/')[-2],
                                trainDir.split(sep='/')[-1],
                                descriptorType, 
                                str(np.average(rocAreas)))
    )

#EOF
