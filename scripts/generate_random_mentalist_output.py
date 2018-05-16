#!/usr/bin/env python

import sys
from random import randint

sample_ids = ["sample-" + str(id) for id in range(0, int(sys.argv[1]))]
locus_ids = ["locus-"+ str(id) for id in range(0, int(sys.argv[2]))]

sequence_types = {}

for sample in sample_ids:
    sequence_types[sample] = []
    for j, locus in enumerate(locus_ids):
        sequence_types[sample].append(randint(0, 9))

print('Sample', '\t'.join(locus_ids), sep='\t')

for sample in sequence_types:
    print(sample, '\t'.join(map(str, sequence_types[sample])), sep='\t')
