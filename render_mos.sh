#!/bin/bash

for id in $(seq 0 29)
do
  python3 render_mos.py --form_id ${id} | tee naturalness_${id}.html
done
