#!/usr/bin/python3

import argparse
import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.style.use("ggplot")
matplotlib.rcParams.update({"font.size" : 15})



parser = argparse.ArgumentParser()
parser.add_argument("resultsFile")
parser.add_argument("compression")
parser.add_argument("scenario")
parser.add_argument("outFile")
args = parser.parse_args()

results = pickle.load(open(args.resultsFile, 'rb'))
print(results)
results = [r for r in results if r["compression"] == args.compression
                             and r["scenario"] == args.scenario]

descriptors = sorted(list(set(r["descriptor"] for r in results)))
compressionRatios = sorted(list(set(r["ratio"] for r in results)))
completeRatios = list(compressionRatios)

for c in compressionRatios:
    for d in descriptors:
        cResults = [r for r in results if r["descriptor"] == d and r["ratio"] == c]
        if cResults == []:
           completeRatios.remove(c) 
           break

compressionRatios = completeRatios
results = [r for r in results if r["ratio"] in compressionRatios]

totalYval = []

for d in descriptors:
    yval = [None] * len(compressionRatios)
    descriptorResults = [r for r in results if r["descriptor"] == d]
    for r in descriptorResults:
        yval[compressionRatios.index(r["ratio"])] = r["avgROCArea"]
    totalYval += yval
    line = plt.plot(compressionRatios, yval, label = d, marker = "o", markersize = 8)
    plt.setp(line, linewidth = 2)


diffYval = max(totalYval) - min(totalYval)

plt.gca().grid(linewidth = 1.5)
plt.gca().set_xlim([0.9 * min(compressionRatios), 1.1 * max(compressionRatios)])
plt.gca().set_ylim([min(totalYval) - 0.1 * diffYval, max(totalYval) + 0.1 * diffYval])
leg = plt.legend(loc = "upper left", fancybox = True)
leg.get_frame().set_alpha(0.5)
plt.gca().set_xscale("log")
plt.gca().set_xticks(compressionRatios)
plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.gca().get_xaxis().set_minor_locator(matplotlib.ticker.NullLocator())

plt.ylabel("Average ROC area")
ratioDescription = "training + query" if args.scenario == "tcqc" else "query only"
plt.xlabel("Compression ratio ({})".format(ratioDescription))
plt.title("Retrieval performance for " + args.compression)
plt.tight_layout()
plt.savefig(args.outFile)
