import sys
import re

rocAreas = []

for l in sys.stdin.readlines():
    m = re.search("rocArea=(\\d+\\.\\d+)", l)
    if m:
        rocAreas.append(float(m.group(1)))

avgArea = sum(rocAreas) / len(rocAreas)
print(avgArea)
