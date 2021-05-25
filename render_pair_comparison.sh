#!/bin/bash

for id in $(seq 0 43)
do
  fid=`expr $id + 30`
  echo "$fid"
  python3 render_pair_comparison.py --form_id ${fid} | tee similarity_${id}.html
done               
