#!/usr/bin/python3

import os, argparse
import subprocess
import pandas as pd
import numpy  as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle
matplotlib.style.use('ggplot')

rootDir    = os.path.dirname(os.path.realpath(__file__))
rawDataDir = os.path.join(rootDir, 'data/raw_dataset')
resultsDir = os.path.join(rootDir, 'results')
resultsFile = os.path.join(resultsDir, 'results.pkl')

results = []

resultParameters = ["descriptor", "fileType", "compressionRatio"]

if  not os.path.exists(rawDataDir):
    print(rawDataDir + " does not exist. Extracting raw_dataset.tar.bz2")
    os.system('tar xvjf ' + rootDir + '/data/raw_dataset.tar.bz2 ' + ' -C ' + rootDir + '/data/');

if not os.path.exists(resultsDir):
    os.mkdir(resultsDir)

if os.path.exists(resultsFile):
    results = pickle.load(open(resultsFile, 'rb'))

parser = argparse.ArgumentParser()
parser.add_argument("doCompression", type = int, default=1)
parser.add_argument("doDescriptors", type = int, default=1)
parser.add_argument("doRetrieval",   type = int, default=1)
parser.add_argument("makePlots",     type = int, default=1)
parser.add_argument("quickTest",     type = str, default=None)
args = parser.parse_args()

if args.quickTest == 'quick':
    compressionRatios = ['100', '200']
    fileTypes         = ['jpg']
    descriptors       = ['orb', 'sift']
else:
    compressionRatios = range(2,100,5)
    fileTypes         = ['jpg', 'jp2', 'jxr']
    descriptors       = ['sift', 'surf', 'brief', 'orb', 'brisk', 'kaze'] # ,'hog']


if args.doDescriptors == True:
    print("computing descriptors for uncompressed pictures...")
    cmdline = os.path.join(rootDir, 'descriptors.py') + ' ' + rawDataDir + ' ' + ','.join(descriptors)
    print(cmdline)
    print()
    subprocess.call(cmdline, shell = True)

for fileType in fileTypes:
    for compressionRatio in compressionRatios:
        print('format={}, ratio={}'.format(fileType, compressionRatio))


        compressedDir = rootDir + '/data/compressed/' + fileType + '/' + str(compressionRatio)
        if args.doCompression == True:
            print('compressing pictures...')
            cmdline = os.path.join(rootDir, 'compress.py') \
                         + ' ' + rawDataDir + ' ' + compressedDir + ' ' \
                         + fileType + ' ' + str(compressionRatio)
            print(cmdline)
            print()
            subprocess.call(cmdline, shell = True)


        if args.doDescriptors == True:
            print('computing descriptors...')
            cmdline = os.path.join(rootDir, 'descriptors.py') \
                        + ' ' + compressedDir + ' ' + ','.join(descriptors)
            print(cmdline)
            print()
            subprocess.call(cmdline, shell = True)


        if args.doRetrieval == True:
            print('doing retrieval...')
            for descriptor in descriptors:
                cmdline = os.path.join(rootDir, 'retrieve.py') \
                        + ' ' + rawDataDir + ' ' + compressedDir + ' ' + descriptor
                print(cmdline)
                print()
                res = subprocess.check_output(cmdline, shell = True)
                res = res.decode('ascii').split(sep='|')
                avgROC = float(res[4].split(sep=':')[1].strip())
                print("avgROC = {}".format(avgROC))
                newResult = {'fileType' : fileType, 'descriptor' : descriptor,
                                'compressionRatio' : compressionRatio,
                                'avgROCArea' : avgROC}
                
                # remove previous results at same parameters
                results = [r for r in results if [r[p] for p in resultParameters]
                        != [newResult[p] for p in resultParameters]]
                
                results.append(newResult)
                # save to disk after every new result
                pickle.dump(results, open(resultsFile, 'wb'))


    if args.makePlots == True:
        print('plotting results...')
        plotResults = [r for r in results if r["fileType"] == fileType
                and r["compressionRatio"] in compressionRatios
                and r["descriptor"] in descriptors]
        
        
        df = pd.DataFrame(np.float,index=range(0,len(compressionRatios)), columns=['ratio']+descriptors)
        for r in plotResults:
            i = compressionRatios.index(int(r["compressionRatio"]))
            df.loc[i, "ratio"] = compressionRatios[i]
            df.loc[i, r["descriptor"]] = r["avgROCArea"]
        
        print(df)
        ax = df.plot(x='ratio', y=descriptors, style='o-')
        plt.ylabel('Average ROC Area')
        plt.xlabel('Compression Ratio')
        plt.title('Retrieval Performance for '+fileType)
        plt.legend(loc='upper left')
        fig = ax.get_figure()
        pdfFileName = 'AvgAreaROC_{}_{}.pdf'.format(fileType, '-'.join(descriptors))
        pdfFile = os.path.join(resultsDir, pdfFileName)
        fig.savefig(pdfFile)
        # avoid remnants of previous plot when drawing multiple plots
        plt.gcf().clear()

#EOF
