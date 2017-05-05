#!/bin/bash
dataDirectory=data/test
descriptors=(sift surf mser fast brief brisk kaze orb)

for descriptor in "${descriptors[@]}"; do
    result=$(python3 retrieve.py $dataDirectory $dataDirectory $descriptor | python3 avgArea.py)
    echo $descriptor $result
done
