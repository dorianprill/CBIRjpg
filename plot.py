#!/usr/bin/python3

import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.style.use("ggplot")
matplotlib.rcParams.update({"font.size" : 15})


def getAvailableValues(parameter):
    return sorted(list(set(r[parameter] for r in results)))


def makePlot(curves, xticks, outFile):
    plt.gcf().clear()
    
    for lineName, lineValues in curves:
        line = plt.plot(range(len(lineValues)), lineValues, label = lineName, marker = "o", markersize = 8)
        plt.setp(line, linewidth = 2)
    
    plt.gca().set_xticks(range(len(xticks)))
    xtickFormatter = matplotlib.ticker.FuncFormatter(lambda x, pos: str(xticks[pos]))
    plt.gca().get_xaxis().set_major_formatter(xtickFormatter)
    plt.gca().get_xaxis().set_minor_locator(matplotlib.ticker.NullLocator())
    
    leg = plt.legend(loc = "upper left", fancybox = True)
    leg.get_frame().set_alpha(0.5)
    
    plt.savefig(outFile)


resultsFile = "results/results.pkl"
results = pickle.load(open(resultsFile, 'rb'))
print("loaded {} results".format(len(results)))

makePlot([("sift", [0.5, 0.4]), ("orb", [0.6, 0.2, 0.1])], [1, 5, 100], "out1.pdf")
