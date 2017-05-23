#!/usr/bin/python3.6

import os, argparse
import subprocess
import pandas as pd
import numpy  as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

rootDir    = os.path.dirname(os.path.realpath(__file__))
rawDataDir = rootDir + '/data/raw_dataset'

if  not os.path.exists(rawDataDir):
    print(rawDataDir + " does not exists. Extracting raw_dataset.tar.bz2")
    os.system('tar xvjf ' + rootDir + '/data/raw_dataset.tar.bz2 ' + ' -C ' + rootDir + '/data/');

parser = argparse.ArgumentParser()
parser.add_argument("doCompression", type = int, default=1)
parser.add_argument("doDescriptors", type = int, default=1)
parser.add_argument("doRetrieval",   type = int, default=1)
parser.add_argument("makePlots",     type = int, default=1)
parser.add_argument("quickTest",     type = str, default=None)
args = parser.parse_args()

if args.quickTest == 'quick':
    compressionRatios = range(2,100,40)
    fileTypes         = ['jpg', 'jp2'] #jp2 is super slow and jxr fails
    descriptors       = ['orb', 'brisk']
else :
    compressionRatios = range(2,100,5)
    fileTypes         = ['jpg', 'jp2', 'jxr']
    descriptors       = ['sift', 'surf', 'brief', 'orb', 'brisk', 'kaze'] # ,'hog']


if args.doDescriptors == True:
    os.system('python3 ' + rootDir + '/descriptors.py ' +  rawDataDir + ' ' + ','.join(descriptors))

for fileType in fileTypes:

    print('file type: {}'.format(fileType))
    # create dataframe for each compression method to plots
    rowidx = 0
    df = pd.DataFrame(np.float,index=range(0,len(compressionRatios)), columns=['ratio']+descriptors)

    for compressionRatio in compressionRatios:

        print('computing for ratio {}...'.format(compressionRatio))

        compressedDir = rootDir + '/data/compressed/' + fileType + '/' + str(compressionRatio)
        if args.doCompression == True:
            os.system('python2.7 ' + rootDir + '/compress.py ' \
                        + rawDataDir + ' ' + compressedDir + ' ' \
                        + fileType + ' ' + str(compressionRatio))

        if args.doDescriptors == True:
            os.system('python3.6 ' + rootDir + '/descriptors.py ' \
                        + compressedDir + ' ' + ','.join(descriptors))

        if args.doRetrieval == True:
            for descriptor in descriptors:
                res = subprocess.check_output(['python3', rootDir + '/retrieve.py',
                                                rawDataDir, compressedDir, descriptor])
                res = res.decode('ascii').split(sep='|')
                df.loc[rowidx,'ratio']    = float(res[2].split(sep=':')[1])
                df.loc[rowidx,descriptor] = float(res[4].split(sep=':')[1][:-2]) # avgRoc  :-2 cuts off '\n'

        # advance index for next compression ratio
        rowidx = rowidx+1

    if args.makePlots == True:
        # plot dataframe with name of compression mode
        ax = df.plot(x='ratio', y=descriptors, style='o-')
        plt.ylabel('Average ROC Area')
        plt.xlabel('Compression Ratio')
        plt.title('Retrieval Performance for '+fileType)
        fig = ax.get_figure()
        fig.savefig('./results/'+'AvgAreaROC'+'_'+fileType+'_'+'-'.join(descriptors)+'.pdf')

#EOF
