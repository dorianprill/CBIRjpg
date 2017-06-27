#!/usr/bin/python3 -u

import os, argparse
import subprocess
import pickle
import re


rootDir    = os.path.dirname(os.path.realpath(__file__))
presetsDir = os.path.join(rootDir, "presets")
datasetDir = os.path.join(rootDir, "data")

results = []


def runCmdline(parts, getOutput = False):
    cmdline = " ".join(parts)
    print(cmdline)
    print()
    if getOutput:
        return subprocess.check_output(cmdline, shell = True).decode("utf-8")
    else:
        subprocess.check_call(cmdline, shell = True)


def compressedPictureDir():
    if cRatio == 1:
        return datasetDir
    compressedDir = os.path.join(rootDir, "data")
    compressedDir = os.path.join(compressedDir, parameters["dataset"] + "_compressed")
    compressedDir = os.path.join(compressedDir, cType)
    compressedDir = os.path.join(compressedDir, str(cRatio))
    return compressedDir


def compressPictures():
    runCmdline([os.path.join(rootDir, "compress.py"),
                datasetDir,
                compressedPictureDir(),
                cType,
                str(cRatio)])


def computeDescriptors(pictureDir):
    runCmdline([os.path.join(rootDir, "descriptors.py"),
                pictureDir,
                ",".join(parameters["descriptors"])])


def getRetrievalScores():
    trainDir = datasetDir if scenario == "tuqc" else compressedPictureDir()
    queryDir = compressedPictureDir()
    output = runCmdline([os.path.join(rootDir, "retrieve.py"),
                queryDir,
                trainDir,
                descriptor], getOutput = True)
    scores = {m.group(1) : float(m.group(2))
              for m in re.finditer("(\\S+):\\s+(\\S+)", output)}
    return scores


def storeResult():
    newResult = {"dataset" : parameters["dataset"],
                 "compressionType" : cType,
                 "compressionRatio" : cRatio,
                 "descriptor" : descriptor,
                 "retrievalScenario" : scenario,
                 "scores" : scores}
    results.append(newResult)
    pickle.dump(results, open(args.resultFile, 'wb'))


def makePlots():
    runCmdline([os.path.join(rootDir, "plot.py")])


# missing: acquire / uncompress datasets

parser = argparse.ArgumentParser()
parser.add_argument("preset")
parser.add_argument("resultFile")
args = parser.parse_args()

if os.path.exists(args.resultFile):
    results = pickle.load(open(args.resultFile, 'rb'))

presetFile = os.path.join(presetsDir, args.preset + ".py")
exec(open(presetFile).read())

datasetDir = os.path.join(datasetDir, parameters["dataset"])

if not results:
    computeDescriptors(datasetDir)


for cType in parameters["compressionTypes"]:
    for cRatio in [r for r in parameters["compressionRatios"][cType] if r > 1]:
        # existing results for this dataset, cType, cRatio
        # => compression has already been done
        if not [r for r in results if  r["dataset"] == parameters["dataset"]
                                   and r["compressionType"] == cType
                                   and r["compressionRatio"] == cRatio]:
            compressPictures()
            computeDescriptors(compressedPictureDir())
        

for cType in parameters["compressionTypes"]:
    for cRatio in [r for r in parameters["compressionRatios"][cType]]:
        for descriptor in parameters["descriptors"]:
            for scenario in parameters["retrievalScenarios"]:
                # existing results for this dataset, cType, cRatio, descriptor, scenario
                # => retrieval has already been done
                if not [r for r in results if  r["dataset"] == parameters["dataset"]
                                           and r["compressionType"] == cType
                                           and r["compressionRatio"] == cRatio
                                           and r["descriptor"] == descriptor
                                           and r["retrievalScenario"] == scenario]:
                    scores = getRetrievalScores()
                    storeResult()
