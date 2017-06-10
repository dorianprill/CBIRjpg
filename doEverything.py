#!/usr/bin/python3

import os, argparse
import subprocess
import pickle

rootDir    = os.path.dirname(os.path.realpath(__file__))
rawDataDir = os.path.join(rootDir, 'data/raw_dataset')
resultsDir = os.path.join(rootDir, 'results')
resultsFile = os.path.join(resultsDir, 'results.pkl')
presetsDir = os.path.join(rootDir, 'presets')

results = []

if  not os.path.exists(rawDataDir):
    print(rawDataDir + " does not exist. Extracting raw_dataset.tar.bz2")
    os.system('tar xvjf ' + rootDir + '/data/raw_dataset.tar.bz2 ' + ' -C ' + rootDir + '/data/');

if not os.path.exists(resultsDir):
    os.mkdir(resultsDir)

if os.path.exists(resultsFile):
    results = pickle.load(open(resultsFile, 'rb'))

parser = argparse.ArgumentParser()
parser.add_argument("doCompression", type = int, nargs = '?', default=1)
parser.add_argument("doDescriptors", type = int, nargs = '?', default=1)
parser.add_argument("doRetrieval",   type = int, nargs = '?', default=1)
parser.add_argument("makePlots",     type = int, nargs = '?', default=1)
parser.add_argument("preset", nargs = '?', default = "quick")
args = parser.parse_args()

presetFile = os.path.join(presetsDir, args.preset + ".py")
exec(open(presetFile).read())

for plot in plots:
    for ratio in plot["ratios"]:
        print('compression={}, ratio={}, scenario = {}'.format(plot["compression"], ratio, plot["scenario"]))

        compressedDir = rootDir + '/data/compressed/' + plot["compression"] + '/' + str(ratio)
        pictureDir = rawDataDir if ratio == 1 else compressedDir
        
        if args.doCompression == True:
            if ratio == 1 or [r for r in results if r["compression"] == plot["compression"] and r["ratio"] == ratio]:
                print("skipping compression")
            else:
                print('compressing pictures...')
                cmdline = os.path.join(rootDir, 'compress.py') \
                             + ' ' + rawDataDir + ' ' + compressedDir + ' ' \
                             + plot["compression"] + ' ' + str(ratio)
                print(cmdline)
                print()
                subprocess.call(cmdline, shell = True)


        if args.doDescriptors == True:
            if [r for r in results if r["compression"] == plot["compression"] and r["ratio"] == ratio]:
                print("skipping descriptor computation")
            else:
                print('computing descriptors...')
                cmdline = os.path.join(rootDir, 'descriptors.py') \
                            + ' ' + pictureDir + ' ' + ','.join(plot["descriptors"])
                print(cmdline)
                print()
                subprocess.call(cmdline, shell = True)


        if args.doRetrieval == True:
            print('doing retrieval...')
            for descriptor in plot["descriptors"]:
                if [    r for r in results if r["compression"] == plot["compression"] and r["ratio"] == ratio
                        and r["descriptor"] == descriptor and r["scenario"] == plot["scenario"]]:
                    print("skipping for descriptor {}".format(descriptor))
                    continue
                trainingDir = rawDataDir if plot["scenario"] == "tuqc" else pictureDir
                cmdline = os.path.join(rootDir, 'retrieve.py') \
                        + ' ' + pictureDir + ' ' + trainingDir + ' ' + descriptor
                print(cmdline)
                print()
                res = subprocess.check_output(cmdline, shell = True)
                res = res.decode('ascii').split(sep='|')
                avgROCArea = float(res[4].split(sep=':')[1].strip())
                print("avgROCArea = {}".format(avgROCArea))
                
                newResult = {"compression" : plot["compression"],
                             "ratio" : ratio,
                             "descriptor" : descriptor,
                             "scenario" : plot["scenario"],
                             "avgROCArea" : avgROCArea}
                
                results.append(newResult)
                # save to disk after every new result
                pickle.dump(results, open(resultsFile, 'wb'))


    if args.makePlots == True:
        print('plotting results...')
        plotFileName = "{}_{}.pdf".format(plot["compression"], plot["scenario"])
        plotFile = os.path.join(resultsDir, plotFileName)
        cmdline = os.path.join(rootDir, 'plot.py') + ' ' \
                + resultsFile + ' ' + plot["compression"] + ' ' \
                + plot["scenario"] + ' ' + plotFile
        print(cmdline)
        print()
        subprocess.call(cmdline, shell = True)

#EOF
