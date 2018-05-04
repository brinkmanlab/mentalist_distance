#!/usr/bin/env python

import argparse
import csv
import itertools
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram, linkage, to_tree

def parse_args():
    parser = argparse.ArgumentParser(description='Calculate distance matrix from MentaLiST MLST output.')
    parser.add_argument('input_file',
                        help='Input file')
    parser.add_argument('-s', '--sep', nargs=1, default='\t',
                        help="Input file field separator")
    parser.add_argument('-q', '--quote', nargs=1, default='"',
                        help="Input file quote char")
    parser.add_argument('-m', '--metric', default='hamming',
                        help="Distance metric")
    parser.add_argument('-f', '--format', default='square',
                        help="Matrix format ('square' or 'triangular')")
    args = parser.parse_args()
    return args


def read_input(input_file, sep, quote):
    """
    Reads csv, returns map of {sample_id: [array of sequence types]}
    input:
      input_file: file path string
      sep: csv separator character (typically '\t' or ',')
      quote: csv quote character
    output:
       ([sample_id], [sequence_type])
    """
    sequence_types = []
    sample_ids = []
    with open(input_file) as f:
        csvreader = csv.reader(f, delimiter=sep, quotechar=quote)
        next(csvreader) # Skip header
        for row in csvreader:
            sample_ids.append(row[0])
            sequence_types.append(row[1:])
    return (sample_ids, sequence_types)

def calculate_distance_matrix(sequence_types):
    """
    Calculate the number of differences between two equal-length lists of symbols.
    If metric=="proportion" then return the proportion, otherwise return the absolute number
    input:
      sequence_types: [[sequence_type]]
      metric: see: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
    output:
      condensed distance matrix
    """
    def distance(xs, ys):
        assert(len(xs) == len(ys))
        d = 0
        for (x, y) in zip(xs, ys):
            if  x != y:
                d += 1
        return d
    return pdist(sequence_types, distance)

def print_distance_matrix(sample_ids, distance_matrix):
    """
    input: 
      sample_ids: [sample_id]
      distance_matrix:  [[distance]]
      format: "square" or "triangular"
    output: none, prints to stdout
    """
    square_distance_matrix = squareform(distance_matrix)
    for i, sample_id in enumerate(sample_ids):
        print(sample_id, square_distance_matrix[i])

def cluster(distance_matrix):
    Z = linkage(distance_matrix, 'average')
    return linked
    
def main():
    args = parse_args()
    sample_ids, sequence_types = read_input(args.input_file, args.sep, args.quote)
    distance_matrix = calculate_distance_matrix(sequence_types)
    print_distance_matrix(sample_ids, distance_matrix)


if __name__ == '__main__':
    main()
