#!/bin/bash
Lines=$(cat req2.txt)
for Line in $Lines
do
    conda skeleton pypi "$Line"
done 

for Line in $Lines
do
    conda-build "$Line"
done 

for Line in $Lines
do
    conda install --use-local "$Line"
done 

conda run --no-capture-output -n myenv python app.py