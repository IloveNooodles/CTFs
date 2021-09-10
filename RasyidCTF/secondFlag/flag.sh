#!/bin/bash

for i in {1..25}
do
	echo "TKWI{j3t0eu_wc4x_n4j_t1gy3i_k3ok}" | caesar $i | grep -i "CTFR"
done
