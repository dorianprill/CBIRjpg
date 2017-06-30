parameters = {
    "dataset" :               "7class",
    "compressionTypes" :     ["jpg", "jp2", "jxr_o0", "jxr_o1", "jxr_o2"],
    "compressionRatios" :    {"jpg" : [1, 2, 10, 50, 100, 150],
                              "jxr_o0" : [1, 2, 10, 50, 100, 150, 300, 450, 600],
                              "jxr_o1" : [1, 2, 10, 50, 100, 150, 300, 450, 600],
                              "jxr_o2" : [1, 2, 10, 50, 100, 150, 300, 450, 600],
                              "jp2" : [1, 2, 10, 50, 100, 150, 300, 450, 600, 900, 1200]},
    "descriptors" :          ["orb", "sift", "surf", "brief", "brisk", "kaze"],
    "retrievalScenarios" :   ["tcqc", "tuqc"]
}
