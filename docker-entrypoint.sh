#!/bin/bash
Lines=$(cat req2.txt)
for Line in $Lines
do
    conda run -n myenv /bin/bash -c conda skeleton pypi "$Line"
done 

for Line in $Lines
do
    conda run -n myenv /bin/bash -c conda-build "$Line"
done 

for Line in $Lines
do
    conda run -n myenv /bin/bash -c conda install --use-local "$Line"
done 

conda run --no-capture-output -n myenv python app.py