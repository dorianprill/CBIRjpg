parameters = {
    "dataset" :               "28class",
    "compressionTypes" :     ["jpg", "jp2", "jxr_o0", "jxr_o1", "jxr_o2"],
    "compressionRatios" :    {"jpg" : [1, 150],
                              "jxr_o0" : [1, 600],
                              "jxr_o1" : [1, 600],
                              "jxr_o2" : [1, 600],
                              "jp2" : [1, 1200]},
    "descriptors" :          ["orb", "sift", "surf", "brief", "brisk", "kaze"],
    "retrievalScenarios" :   ["tcqc", "tuqc"]
}
