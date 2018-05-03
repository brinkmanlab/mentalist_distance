#!/usr/bin/env python

import argparse
import csv
import itertools

def parse_args():
    parser = argparse.ArgumentParser(description='Calculate distance matrix from MentaLiST MLST output.')
    parser.add_argument('input_file',
                        help='Input file')
    parser.add_argument('-s', '--sep', nargs=1, default='\t',
                        help="Input file field separator")
    parser.add_argument('-q', '--quote', nargs=1, default='"',
                        help="Input file quote char")
    parser.add_argument('-m', '--metric', default='count',
                        help="Distance metric ('proportion' or 'count')")
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

def calculate_distance(sample_1_sts, sample_2_sts, metric="count"):
    """
    Calculate the number of differences between two equal-length lists of symbols.
    If metric=="proportion" then return the proportion, otherwise return the absolute number
    input:
      sample_1_sts: [sequence type]
      sample_2_sts: [sequence type]
      metric: "count" or "proportion"
    output:
      distance between samples (numeric)
    """
    assert len(sample_1_sts) == len(sample_2_sts)
    total_sts = len(sample_1_sts)
    different_sts = 0
    for sample_1_st, sample_2_st in zip(sample_1_sts, sample_2_sts):
        if sample_1_st != sample_2_st:
            different_sts += 1
    if metric == "count":
        return different_sts
    elif metric == "proportion":
        return different_sts / total_sts

def generate_distance_matrix(sample_ids, sequence_types, metric):
    """
    input:
      sample_ids: [sample_id]
      sequence_types: [[sequence_type]]}
      metric: "count" or "proportion"
    output:
      distance_matrix: dict {sample_id: [distances]}
    """
    distance_matrix = []
    for i, sample_1 in enumerate(sample_ids):
        distance_row = []
        for j, sample_2 in enumerate(sample_ids):
            distance_row.append(calculate_distance(sequence_types[i], sequence_types[j], metric))
        distance_matrix.append(distance_row)
    return distance_matrix

def print_output(sample_ids, distance_matrix, format):
    """
    input: 
      sample_ids: [sample_id]
      distance_matrix:  [[distance]]
      format: "square" or "triangular"
    output: none, prints to stdout
    """
    print(len(sample_ids))
    for i, sample_id in enumerate(sample_ids):
        print(sample_id, end=" ")
        if format == "square":
            distance_row = distance_matrix[i]
        elif format == "triangular":
            distance_row = distance_matrix[i][:i]
        print(" ".join("%.8f" % i for i in distance_row))
    
    
def main():
    args = parse_args()
    sample_ids, sequence_types = read_input(args.input_file, args.sep, args.quote)
    distance_matrix = generate_distance_matrix(sample_ids, sequence_types, args.metric)
    print_output(sample_ids, distance_matrix, args.format)

if __name__ == '__main__':
    main()
