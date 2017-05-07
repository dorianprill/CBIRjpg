import os, argparse

rootDir = os.path.dirname(os.path.realpath(__file__))

rawDataDir = rootDir + '/data/raw_dataset'

if  not os.path.exists(rawDataDir):
    print(rawDataDir + " does not exists. Extracting raw_dataset.tar.bz2")
    os.system('tar xvjf ' + rootDir + '/data/raw_dataset.tar.bz2 ' + ' -C ' + rootDir + '/data/');


fileTypes = ['jpg', 'jp2', 'jxr']
compressionRatios = range(2,100,5)
descriptors = ['sift', 'surf', 'brief', 'orb', 'brisk', 'kaze']

parser = argparse.ArgumentParser()
parser.add_argument("doCompression", type = int, default=1)
parser.add_argument("doDescriptors", type = int, default=1)
parser.add_argument("doRetrieval", type = int, default=1)
args = parser.parse_args()


if args.doDescriptors == True:
    for descriptor in descriptors:
        os.system('python3 ' + rootDir + '/descriptors.py ' +  rawDataDir + ' ' + descriptor)

for fileType in fileTypes:
    for compressionRatio in compressionRatios:
        compressedDir = rootDir + '/data/compressed/' + fileType + '/' + str(compressionRatio)
        if args.doCompression == True:
            os.system('python ' + rootDir + '/compress.py ' + rawDataDir + ' ' + compressedDir + ' ' + fileType + ' ' + str(compressionRatio))

        if args.doDescriptors == True:
            for descriptor in descriptors:
                os.system('python3 ' + rootDir + '/descriptors.py ' +  compressedDir + ' ' + descriptor)

        if args.doRetrieval == True:
            for descriptor in descriptors:
                os.system('python3 ' + rootDir + '/retrieve.py ' + rawDataDir + ' ' + compressedDir + ' ' + descriptor)