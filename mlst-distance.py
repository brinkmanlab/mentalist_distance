#!/usr/bin/env/python

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
    parser.add_argument('-m', '--metric', default='absolute',
                        help="Distance metric ('proportion' or 'absolute')")
    args = parser.parse_args()
    return args


def read_input(input_file, sep, quote):
    """
    Reads csv, returns map of {sample_id: [array of sequence types]} 
    """
    sample_data = {}
    with open(input_file) as f:
        csvreader = csv.reader(f, delimiter=sep, quotechar=quote)
        next(csvreader) # Skip header
        for row in csvreader:
            sample_data[row[0]] = row[1:]
    
    return sample_data

def calculate_distance(sample_1_sts, sample_2_sts, metric="absolute"):
    assert len(sample_1_sts) == len(sample_2_sts)
    total_sts = len(sample_1_sts)
    different_sts = 0
    for sample_1_st, sample_2_st in zip(sample_1_sts, sample_2_sts):
        if sample_1_st != sample_2_st:
            different_sts += 1
    if metric == "absolute":
        return different_sts
    elif metric == "proportion":
        return different_sts / total_sts

def generate_distance_matrix(sample_data, metric):
    """
    distance_matrix is dict {(sample_1_id, sample_2_id): distance}
    """
    distance_matrix = {}
    for sample_1, sample_2 in itertools.combinations(sample_data, 2):
        distance_matrix[(sample_1, sample_2)] = calculate_distance(sample_data[sample_1], sample_data[sample_2], metric)
    return distance_matrix

def print_output(distance_matrix):
    """
    distance_matrix is dict {(sample_1_id, sample_2_id): distance}
    """
    sample_ids = sorted(set(list(sum(distance_matrix.keys(), ()))))
    print(len(sample_ids))
    for sample_id_1 in sample_ids:
        print(sample_id_1, end=" ")
        distance_row = []
        for sample_id_2 in sample_ids:
            try:
                distance_row.append(distance_matrix[sample_id_2, sample_id_1])
            except KeyError:
                continue
        print(" ".join("%.8f" % i for i in distance_row))
    
    
def main():
    args = parse_args()
    sample_data = read_input(args.input_file, args.sep, args.quote)
    distance_matrix = generate_distance_matrix(sample_data, args.metric)
    print_output(distance_matrix)

if __name__ == '__main__':
    main()
