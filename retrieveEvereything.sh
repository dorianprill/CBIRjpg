#!/bin/bash
for D in data/*; do for sd in data/*; do for ssd in $sd/*; do 
echo $ssd
python3 retrieve.py ../../raw_dataset/ $ssd sift | grep total | cut -d " " -f 4 | paste -sd+ | bc; 
python3 retrieve.py ../../raw_dataset/ $ssd surf | grep total | cut -d " " -f 4 | paste -sd+ | bc;
python3 retrieve.py ../../raw_dataset/ $ssd kaze | grep total | cut -d " " -f 4 | paste -sd+ | bc;
python3 retrieve.py ../../raw_dataset/ $ssd brief | grep total | cut -d " " -f 4 | paste -sd+ | bc;
python3 retrieve.py ../../raw_dataset/ $ssd brisk | grep total | cut -d " " -f 4 | paste -sd+ | bc;
python3 retrieve.py ../../raw_dataset/ $ssd orb | grep total | cut -d " " -f 4 | paste -sd+ | bc;

done; done; done