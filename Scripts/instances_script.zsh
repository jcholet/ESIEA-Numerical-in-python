#!/bin/zsh

# This script is used to create lp files from instances
for i in {1..10}; do
    input="../Instances/small/instance$i.txt"
    output="../Fichiers LP/instance$i.lp"
    python3 ../convertion.py $input $output
    wait
done