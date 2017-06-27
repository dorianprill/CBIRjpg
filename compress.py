#!/usr/bin/python3

import os, subprocess, argparse
import numpy as np

class Encoder:
    def __init__(self, inFile, encFile, decFile):
        self.inFile = inFile
        self.encFile = encFile
        self.decFile = decFile

    def encode(self, quality):
        if os.path.exists(self.encFile):
            os.remove(self.encFile)
        parameters = (self.inFile, self.encFile, self.qualityRange[quality])
        subprocess.call(self.encCmdline.format(*parameters), shell = True,
                stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
        return os.path.getsize(self.encFile)
    
    def decode(self):
        if os.path.exists(self.decFile):
            os.remove(self.decFile)
        parameters = (self.encFile, self.decFile)
        subprocess.call(self.decCmdline.format(*parameters), shell = True,
                stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)


class JPGEncoder(Encoder):
    fileEnding = ".jpg"
    qualityRange = range(0, 101)
    encCmdline = "gm convert {0} -quality {2} {1}"
    decCmdline = "gm convert {0} {1}"

class JP2Encoder(Encoder):
    fileEnding = ".jp2"
    qualityRange = range(5000, 0, -1)
    encCmdline = "opj_compress -i {0} -o {1} -r {2}"
    decCmdline = "opj_decompress -i {0} -o {1}"

class JXREncoder(Encoder):
    fileEnding = ".jxr"
    # use quantization (integer) quality levels
    # this means worse results, but more available compression levels
    qualityRange = range(255, 0, -1)
    encCmdline = "JxrEncApp -i {0} -o {1} -q {2}"
    decCmdline = "JxrDecApp -i {0} -o {1}"

class NoOverlapJXREncoder(JXREncoder):
    encCmdline = "JxrEncApp -i {0} -o {1} -q {2} -l 0"

class OneOverlapJXREncoder(JXREncoder):
    encCmdline = "JxrEncApp -i {0} -o {1} -q {2} -l 1"

class TwoOverlapJXREncoder(JXREncoder):
    encCmdline = "JxrEncApp -i {0} -o {1} -q {2} -l 2"   

def calculateTargetSize(inFile, compressionRatio):
  originalSize = os.path.getsize(inFile)
  targetSize = originalSize // compressionRatio
  return (originalSize, targetSize)


def compressToSize(encoder, targetSize):
    lowerIdx, currentIdx, upperIdx = 0, 0, len(encoder.qualityRange) - 1
    while lowerIdx <= upperIdx:
        currentIdx = (lowerIdx + upperIdx) // 2
        outFileSize = encoder.encode(currentIdx)
        if outFileSize <= targetSize:
            lowerIdx = currentIdx + 1
        else:
            upperIdx = currentIdx - 1
    
    outFileSize = encoder.encode(currentIdx)
    
    if outFileSize <= targetSize:
        return (currentIdx, outFileSize)
    elif currentIdx > 0:
        currentIdx -= 1
    else:
        currentIdx = 0
    
    outFileSize = encoder.encode(currentIdx)
    return (currentIdx, outFileSize)



formatChoices = {"jpg" : JPGEncoder, "jp2" : JP2Encoder, "jxr" : JXREncoder, "0jxr" : NoOverlapJXREncoder,
                  '1jxr' : OneOverlapJXREncoder, '2jxr' : TwoOverlapJXREncoder}

parser = argparse.ArgumentParser()
parser.add_argument("inDirectory")
parser.add_argument("outDirectory")
parser.add_argument("fileFormat", choices = formatChoices.keys())
parser.add_argument("compressionRatio", type = int)
args = parser.parse_args()

chosenEncoder = formatChoices[args.fileFormat]

if not os.path.exists(args.outDirectory):
    print("Warning: The output directory you specified does not exist. It will now be created.")
    os.makedirs(args.outDirectory)

for subdir, dirs, files in sorted(os.walk(args.inDirectory)):
    for pictureFileName in [f for f in sorted(files) if f.endswith(".bmp")]:
        pictureFile = os.path.join(subdir, pictureFileName)
        outDir = os.path.join(args.outDirectory, os.path.relpath(subdir, args.inDirectory))
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        encPictureFileName = os.path.splitext(pictureFileName)[0] + chosenEncoder.fileEnding
        encPictureFile = os.path.join(outDir, encPictureFileName)
        decPictureFile = encPictureFile + ".bmp"
        originalSize, targetSize = calculateTargetSize(pictureFile, args.compressionRatio)
        encoder = chosenEncoder(pictureFile, encPictureFile, decPictureFile)
        encQuality, encPictureSize = compressToSize(encoder, targetSize)
        encRatio = originalSize / encPictureSize
        encoder.decode()
        print("{} quality = {} size = {} ratio = {:5f}".format(pictureFileName,
                                                            encoder.qualityRange[encQuality],
                                                            encPictureSize,
                                                            encRatio))
        if encPictureSize > targetSize:
            raise Exception("could not meet target size!")
