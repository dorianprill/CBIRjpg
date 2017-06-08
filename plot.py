#!/usr/bin/python3

import argparse
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


parser = argparse.ArgumentParser()
parser.add_argument("resultsFile")
parser.add_argument("fileType")
parser.add_argument("outFile")
args = parser.parse_args()


results = pickle.load(open(args.resultsFile, 'rb'))

print(results)

plotResults = [r for r in results if r["fileType"] == args.fileType]
descriptors = sorted(list(set(r["descriptor"] for r in results)))
compressionRatios = sorted(list(set(int(r["compressionRatio"]) for r in results)))
print(descriptors)
print(compressionRatios)

df = pd.DataFrame(np.float, index = range(len(compressionRatios)), columns = ['ratio'] + descriptors)
for r in plotResults:
    i = compressionRatios.index(int(r["compressionRatio"]))
    df.loc[i, "ratio"] = compressionRatios[i]
    df.loc[i, r["descriptor"]] = r["avgROCArea"]

print(df)
ax = df.plot(x = 'ratio', y = descriptors, style = 'o-')
plt.ylabel('Average ROC Area')
plt.xlabel('Compression Ratio')
plt.title('Retrieval Performance for ' + args.fileType)
plt.legend(loc='upper left')
fig = ax.get_figure()
fig.savefig(args.outFile)
