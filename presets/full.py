parameters = {
    "dataset" :               "28class",
    "compressionTypes" :     ["jpg", "jp2", "jxr"],
    "compressionRatios" :    {"jpg" : [1, 2, 10, 50, 100, 150],
                              "jxr" : [1, 2, 10, 50, 100, 150, 300, 450, 600],
                              "jp2" : [1, 2, 10, 50, 100, 150, 300, 450, 600, 900, 1200]},
    "descriptors" :          ["orb", "sift", "surf", "brief", "brisk", "kaze"],
    "retrievalScenarios" :   ["tcqc", "tuqc"]
}
