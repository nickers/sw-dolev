#!/bin/bash

echo "digraph test{ " > graph.txt
python master-node.py $1 >> graph.txt 
echo "}" >> graph.txt 
dot -o gg.png -Tpng graph.txt
display gg.png
