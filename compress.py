import os, sys, uuid, argparse, math

def calculateTargetSize(inFile, compressionRatio):
  originalSize = os.path.getsize(inFile)
  return math.floor(originalSize / compressionRatio)

def encodeGM(inFile, outFile, quality):
  os.system("gm convert {} -quality {} {}".format(inFile, quality, outFile))

def encodeJpeg2000(inFile, outFile, quality):
  os.system("opj_compress -i {} -r {} -o {}".format(inFile, quality, outFile))

def decodeGM(inFile, outFile):
  os.system("gm convert {} {}".format(inFile, outFile))

def encodeJxrLib(inFile, outFile, quality):
  os.system("JxrEncApp -i {} -o {} -q {}".format(inFile, outFile, quality))

def preprocessImage(fileName):
  originalUncompressed = str(uuid.uuid4()) + ".bmp"
  decodeGM(fileName, originalUncompressed)
  return originalUncompressed

def compressorFunction(encoder, inFile, filePrefix, fileEnding, qualityRange):
  def compress(encoder, inFile, filePrefix, fileEnding, qualityRange, qualityIdx):
    quality = qualityRange[qualityIdx]
    outFile = "{}_{}{}".format(filePrefix, str(quality), fileEnding)
    encoder(inFile, outFile, quality)
    outFileSize = os.path.getsize(outFile)
    return (outFile, outFileSize)

  return lambda qualityIdx : compress(encoder, inFile, filePrefix, fileEnding, qualityRange, qualityIdx)

def compressToSize(encoder, inFile, fileEnding, qualityRange, compressionRatio):
  targetSize = calculateTargetSize(inFile, compressionRatio)
  filePrefix = str(uuid.uuid4())
  lowerIdx, currentIdx, upperIdx = 0, 0, len(qualityRange) - 1
  compressAtQuality = compressorFunction(encoder, inFile, filePrefix, fileEnding, qualityRange)

  while lowerIdx <= upperIdx:
    currentIdx = (lowerIdx + upperIdx) / 2
    outFile, outFileSize = compressAtQuality(currentIdx)
    os.remove(outFile)
    if outFileSize <= targetSize:
      lowerIdx = currentIdx + 1
    else:
      upperIdx = currentIdx - 1

  outFile, outFileSize = compressAtQuality(currentIdx)
  if outFileSize <= targetSize:
    return (outFile, qualityRange[currentIdx], outFileSize)
  elif currentIdx > 0:
    currentIdx -= 1
  else:
    currentIdx = 0

  os.remove(outFile)
  outFile, outFileSize = compressAtQuality(currentIdx)
  return (outFile, qualityRange[currentIdx], outFileSize)

def switchExtension(fileName, newExtension):
  baseName, extension = os.path.splitext(fileName)
  return baseName + newExtension

def convertImagesInDirectory(inDir, outDir, compressor):
  dirList = os.listdir(inDir)
  for i in range(len(dirList)):
    originalFile = os.path.join(inDir, dirList[i])
    if originalFile.endswith('.bmp'):
      print(originalFile)
      uncompressedOriginal = str(uuid.uuid4()) + ".bmp"
      print(uncompressedOriginal)
      decodeGM(originalFile, uncompressedOriginal)
      compressedFile, quality, fileSize = compressor.compress(uncompressedOriginal)
      compressedFileName = switchExtension(os.path.split(originalFile)[1], compressor.extension)
      os.rename(compressedFile, os.path.join(outDir, compressedFileName))
      os.remove(uncompressedOriginal)
      print("{}/{} {} q = {} size = {}".format(i + 1, len(dirList), dirList[i], quality, fileSize))
      targetSize = calculateTargetSize(originalFile, compressor.compressionRatio)
      if fileSize > targetSize:
        print("could not meet target size!")
        sys.exit(1)

class JPGFormat:
  def __init__(self, compressionRatio):
    self.compressionRatio = compressionRatio
    self.qualityRange = range(1, 150)
    self.extension = ".jpg"

  def compress(self, inFileName):
    return compressToSize(encodeGM, inFileName, self.extension, self.qualityRange, self.compressionRatio)

class JP2Format:
  def __init__(self, compressionRatio):
    self.compressionRatio = compressionRatio
    self.qualityRange = range(300, 1, -1  )
    self.extension = ".jp2"

  def compress(self, inFileName):
    return compressToSize(encodeJpeg2000, inFileName, self.extension, self.qualityRange, self.compressionRatio)

class JXRFormat:
  def __init__(self, compressionRatio):
    self.compressionRatio = compressionRatio
    self.qualityRange = range(150, 1, -1)
    self.extension = ".jxr"

  def compress(self, inFileName):
    return compressToSize(encodeJxrLib, inFileName, self.extension, self.qualityRange, self.compressionRatio)

formatChoices = {"jpg" : JPGFormat, "jp2" : JP2Format, "jxr" : JXRFormat}

parser = argparse.ArgumentParser()
parser.add_argument("inDirectory")
parser.add_argument("outDirectory")
parser.add_argument("fileFormat", choices = formatChoices.keys())
parser.add_argument("compressionRatio", type = int)
args = parser.parse_args()

compressor = formatChoices[args.fileFormat](args.compressionRatio)

if not os.path.exists(args.outDirectory):
  print("Warning: The output directory you specified does not exist. It will now be created.")
  os.makedirs(args.outDirectory)

for subdir, dirs, files in os.walk(args.inDirectory):
    for directory in dirs:
      outSubDir = os.path.join(args.outDirectory, directory)
      inSubDir  = os.path.join(args.inDirectory, directory)
      if not os.path.exists(outSubDir):
        os.makedirs(outSubDir)
      print('directory: ' + inSubDir)
      print('subdir:' + outSubDir)
      convertImagesInDirectory(inSubDir, outSubDir, compressor)
