#!/usr/bin/env python

import argparse
import csv
import numpy as np
from scipy.spatial.distance import pdist, squareform

def parse_args():
    parser = argparse.ArgumentParser(description='Calculate distance matrix from MentaLiST MLST output.')
    parser.add_argument('input',
                        help='Input file')
    parser.add_argument('-s', '--sep', nargs=1, default='\t',
                        help="Input file field separator")
    parser.add_argument('-q', '--quote', nargs=1, default='"',
                        help="Input file quote char")
    parser.add_argument('-e', '--exclude',
                        help="Comma-separated list of labels for columns to exclude")
    args = parser.parse_args()
    return args


def read_input(input_file, excluded, sep='\t', quote='"'):
    """
    Reads csv, returns tuple ([sample_id], [[sequence_type]]
    input:
      input_file: file path string
      sep: csv separator character (typically '\t' or ',')
      quote: csv quote character
      excluded: headers of columns to exclude from sequence type matrix
    output:
       ([sample_id], [[sequence_type]])
    """
    sequence_types = []
    sample_ids = []
    with open(input_file) as f:
        csvreader = csv.reader(f, delimiter=sep, quotechar=quote)
        header = next(csvreader)
        excluded_idxs = {0}
        for idx, label in enumerate(header):
            if label in excluded:
                excluded_idxs.add(idx)
        for row in csvreader:
            sample_ids.append(row[0])
            sequence_types.append([element for idx, element in enumerate(row) if idx not in excluded_idxs])
    return (sample_ids, sequence_types)

def calculate_distance_matrix(sequence_types):
    """
    Calculate the number of differences between two equal-length lists of symbols.
    If metric=="proportion" then return the proportion, otherwise return the absolute number
    input:
      sequence_types: [[sequence_type]]
      metric: see: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
    output:
      condensed distance matrix (numpy ndarray)
    """
    def hamming_distance(xs, ys):
        assert(len(xs) == len(ys))
        d = 0
        for (x, y) in zip(xs, ys):
            if  x != y:
                d += 1
        return d
    return pdist(sequence_types, hamming_distance)

def print_distance_matrix(sample_ids, distance_matrix):
    """
    input: 
      sample_ids: [sample_id]
      distance_matrix:  numpy ndarray
    output: none, prints to stdout
    """
    square_distance_matrix = squareform(distance_matrix)
    print(len(sample_ids))
    for i, sample_id in enumerate(sample_ids):
        print(sample_id, ' '.join(map(str, square_distance_matrix[i])), sep=' ')
    
def main():
    args = parse_args()
    excluded_labels = set(['ST', 'clonal_complex'])
    if args.exclude:
        excluded_labels |= set(args.exclude.split(','))
    sample_ids, sequence_types = read_input(args.input, excluded_labels, args.sep, args.quote)
    distance_matrix = calculate_distance_matrix(sequence_types)
    print_distance_matrix(sample_ids, distance_matrix.astype(int))


if __name__ == '__main__':
    main()
