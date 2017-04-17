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
    imagesToRetrieve = 5
    flann = cv2.FlannBasedMatcher(index_params,search_params)


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
                                if m.distance < 0.70*n.distance:
                                    goodMatches.append(m)
    
                            distances = list(map(lambda m: m.distance, goodMatches))
                            result =  (np.average(distances), subdir2.split('/')[-1])
                            print('result: ' + str(result))
                            results.append(result)

                print("queryType: " + queryType)
                correctImages = len(list(filter(lambda r: r[1] == queryType , sorted(results)[:imagesToRetrieve])))

                print("total: " + str(imagesToRetrieve) + " found: " + str(correctImages))

                print(sorted(results))