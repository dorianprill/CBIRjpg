import  cv2
import  sys
import  os
import  pickle
import  numpy as np


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
    dataDir = sys.argv[2]
    descriptor = sys.argv[3]
    
    if descriptor == 'sift' or descriptor == 'surf':
        bf = cv2.BFMatcher()
    else:
        bf = cv2.BFMatcher(normType=cv2.NORM_HAMMING)
  
    imagesToRetrieve = 3

    for subdir, dirs, files in os.walk(queryDir):
        for file in files:
            queryFilename = os.path.join(subdir, file)
            if file.endswith('.' + descriptor):
                print('queryDes:' + queryFilename);
                queryDes = pickle.load(open(queryFilename, 'rb'))
                queryType = queryFilename.split('/')[-2]
                goodMatches = []
                results = []
                
                for subdir2, dirs, files2 in os.walk(dataDir):
                    for file2 in files2:
                        if file2.endswith('.' + descriptor):
                            # find the keypoints and compute descriptors
                            print('des: ' + os.path.join(subdir2, file2))
                            des = pickle.load(open(os.path.join(subdir2, file2), 'rb'))
                            matches = bf.knnMatch(queryDes, des, k=2)
                            for m,n in matches:
                                if m.distance < 0.75*n.distance:
                                    goodMatches.append(m)

                            distances = list(map(lambda m: m.distance, goodMatches))
                            result =  (np.average(distances), subdir2.split('/')[-1])
                            print('result: ' + str(result))
                            results.append(result)

                print("queryType: " + queryType)
                correctImages = len(list(filter(lambda r: r[1] == queryType , sorted(results)[:imagesToRetrieve])))

                print("total: " + str(imagesToRetrieve) + " found: " + str(correctImages))

                print(sorted(results))