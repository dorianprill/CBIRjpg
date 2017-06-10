#!/bin/sh
for f in results/*.pdf; do
    bn=$(basename -s .pdf $f)
    ppmn=results/$bn.ppm
    pdftoppm -rx 200 -ry 200 $f > $ppmn
    pngn=results/png/$bn.png
    gm convert $ppmn -resize x640 $pngn
    rm $ppmn
done
