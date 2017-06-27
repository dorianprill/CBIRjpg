#!/usr/bin/python3

import pickle
import matplotlib
import argparse
from itertools import product

matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.style.use("ggplot")
matplotlib.rcParams.update({"font.size" : 10})


def getAvailableValues(parameter):
    return sorted(list(set(r[parameter] for r in results)))


def getAvailableScoreTypes():
    scoreTypes = [r["scores"].keys() for r in results]
    return sorted(list(set(t for st in scoreTypes for t in st)))


def getCompressionRatios(parameters):
    filteredResults = results[:]
    for param, value in parameters:
        filteredResults = [r for r in filteredResults if r[param] == value]
    
    return sorted(list(set(r["compressionRatio"] for r in filteredResults)))


def getScore(parameters, scoreType):
    filteredResults = results[:]
    for param, value in parameters:
        filteredResults = [r for r in filteredResults if r[param] == value]
    
    if len(filteredResults) == 0:
        return None
    elif len(filteredResults) == 1:
        return filteredResults[0]["scores"][scoreType]
    else:
        raise Exception("multiple results for given parameters")


def makePlot(curves, xticks, yLimits, xLabel, yLabel, title, outFile):
    plt.gcf().clear()
    
    for lineName, lineValues in curves:
        xValues = [i for i in range(len(lineValues)) if lineValues[i] is not None]
        yValues = [v for v in lineValues if v is not None]
        line = plt.plot(xValues, yValues, label = lineName, marker = "o", markersize = 8)
        plt.setp(line, linewidth = 2)
    
    plt.xlim([-0.1, len(xticks) - 0.9])
    plt.ylim(yLimits)
    
    plt.gca().grid(linewidth = 1.5)
    
    plt.gca().set_xticks(range(len(xticks)))
    xtickFormatter = matplotlib.ticker.FuncFormatter(lambda x, pos: str(xticks[pos]))
    plt.gca().get_xaxis().set_major_formatter(xtickFormatter)
    plt.gca().get_xaxis().set_minor_locator(matplotlib.ticker.NullLocator())
    
    leg = plt.legend(loc = "upper left", fancybox = True)
    leg.get_frame().set_alpha(0.5)
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    
    plt.tight_layout()
    
    plt.savefig(outFile)



parser = argparse.ArgumentParser()
parser.add_argument("resultsFile")
args = parser.parse_args()

results = pickle.load(open(args.resultsFile, 'rb'))
print("loaded {} results".format(len(results)))

exec(open("plotLimits.py").read())

plotCounter = 0


# compressionType - specific plots
for dataset, cType, scenario, scoreType in product(getAvailableValues("dataset"),
                                                   getAvailableValues("compressionType"),
                                                   getAvailableValues("retrievalScenario"),
                                                   getAvailableScoreTypes()):
    parameters = [("dataset", dataset), ("compressionType", cType),
                  ("retrievalScenario", scenario)]
    outFile = "results/c_{}_{}_{}_{}.png".format(dataset, scoreType, scenario, cType)
    xticks = getCompressionRatios(parameters)
    curves = []
    
    for descriptor in getAvailableValues("descriptor"):
        values = []
        for cRatio in xticks:
            fullParameters = parameters + [("descriptor", descriptor), ("compressionRatio", cRatio)]
            values.append(getScore(fullParameters, scoreType))
        curves.append((descriptor, values))
    
    xlabel = "Compression ratio (query only)" if scenario == "tuqc" else \
             "Compression ratio (training + query)"
    ylabel = scoreType + " score"
    title = "compression: " + cType
    makePlot(curves, xticks, yLimits[scoreType], xlabel, ylabel, title, outFile)
    plotCounter += 1


print("generated {} compression-specific plots".format(plotCounter))
plotCounter = 0


# descriptor - specific plots
for dataset, descriptor, scenario, scoreType in product(getAvailableValues("dataset"),
                                                        getAvailableValues("descriptor"),
                                                        getAvailableValues("retrievalScenario"),
                                                        getAvailableScoreTypes()):
    parameters = [("dataset", dataset), ("descriptor", descriptor),
                  ("retrievalScenario", scenario)]
    outFile = "results/d_{}_{}_{}_{}.png".format(dataset, scoreType, scenario, descriptor)
    xticks = getCompressionRatios(parameters)
    curves = []
    
    for cType in getAvailableValues("compressionType"):
        values = []
        for cRatio in xticks:
            fullParameters = parameters + [("compressionType", cType), ("compressionRatio", cRatio)]
            values.append(getScore(fullParameters, scoreType))
        curves.append((cType, values))
    
    xlabel = "Compression ratio (query only)" if scenario == "tuqc" else \
             "Compression ratio (training + query)"
    ylabel = scoreType + " score"
    title = "descriptor: " + descriptor
    makePlot(curves, xticks, yLimits[scoreType], xlabel, ylabel, title, outFile)
    plotCounter += 1


print("generated {} descriptor-specific plots".format(plotCounter))
