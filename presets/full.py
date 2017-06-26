parameters = {
    "dataset" :               "28class",
    "compressionTypes" :     ["jpg", "jp2", "jxr"],
    "compressionRatios" :    {"jpg" : [1, 2, 20, 50, 100, 250], "jp2" : [1, 2, 20, 50, 100, 250, 500, 800, 1200], "jxr" : [1, 2, 20, 50, 100, 250, 500, 800]},
    "descriptors" :          ["orb", "sift", "surf", "brief", "brisk", "kaze"],
    "retrievalScenarios" :   ["tcqc", "tuqc"]
}
