#!/bin/bash

for id in $(seq 0 49)
do
  python3 render_pair_comparison.py --form_id ${id} | tee similarity_${id}.html
done               
