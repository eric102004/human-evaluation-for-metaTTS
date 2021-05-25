#!/bin/bash

for id in $(seq 0 43)
do
  python3 render_pair_comparison.py --form_id ${id+30} | tee similarity_${id}.html
done               
