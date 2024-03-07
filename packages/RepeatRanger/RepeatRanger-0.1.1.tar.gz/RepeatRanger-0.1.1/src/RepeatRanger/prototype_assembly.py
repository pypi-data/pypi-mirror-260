#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 02.02.2024
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

import argparse

from trseeker.seqio.fasta_file import sc_iter_fasta_brute
from tqdm import tqdm
from trseeker.tools.sequence_tools import get_revcomp
from intervaltree import IntervalTree
from RepeatRanger.tools.graph import build_fs_tree_from_sequence, build_fs_left_tree_from_sequence
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_fasta(fasta_file, spacer="NNN"):
    array = []
    pos2header = IntervalTree()
    start = 0
    for header, seq in sc_iter_fasta_brute(fasta_file):
        array.append(seq.upper())
        end = start + len(seq) + 3
        pos2header.addi(start, end, header[1:])
        start = end
    array = spacer.join(array)
    return array, pos2header

def get_kmer_positions(array, kmer):
    names_ = []
    positions_ = []
    k = 23
    start = 0
    while True:
        pos = array.find(kmer, start)
        if pos == -1:
            break
        names_.append(pos)
        positions_.append(pos)  
        start = pos + 1
    return names_, positions_

def get_loci(abrupted_left_nodes, abrupted_nodes, array, names_):
    sequences = []
    pair_sequences = []
    for node in names_:
        start = abrupted_left_nodes[node][0]
        end = abrupted_nodes[node][0]
        L = end - start
        status_L = abrupted_left_nodes[node][1]
        status_R = abrupted_nodes[node][1]
        sequences.append((L, start, end, status_L, status_R, array[start:end]))
        pair_sequences.append((
            (node-start, start, node, status_L, "ORI", array[start:node]),
            (end-node, node, end, "ORI", status_R, array[node:end])
        ))
    pair_sequences.sort(reverse=True)
    sequences.sort(reverse=True)
    return sequences, pair_sequences

def join_overlapping_loci(sequences, array):
    itree = IntervalTree()
    for jj, (L, start, end, status_L, status_R, seq) in enumerate(sequences):
        itree.addi(start, end)
    itree.merge_overlaps()
    joined_sequences = []
    for item in itree:
        start = item.begin
        end = item.end
        L = end - start
        joined_sequences.append((L, start, end, array[start:end]))
    joined_sequences.sort(reverse=True)
    return joined_sequences

def parse_arguments():
    parser = argparse.ArgumentParser(description='Find all repeats loci according to seed kmers.')
    parser.add_argument('-f', help='Fasta file', required=True)
    parser.add_argument('-o', help='Output fasta file', required=True)
    parser.add_argument('-i', help='Seed kmer', required=True)
    parser.add_argument('-c', help='Cutoff [1]', required=False, default=1, type=int)
    return parser.parse_args()

def save_loci(joined_sequences, pos2header, output_file):
    with open(output_file, "w") as fw:
        for L, start, end, seq in joined_sequences:
            chromosomes = list(pos2header[start:end])
            assert len(chromosomes) == 1
            chrm = chromosomes[0].data.split()[0]
            chrm_start = chromosomes[0].begin
            fw.write(f">{L}_{chrm}_{start-chrm_start}_{end-chrm_start}\n{seq}\n")


def main():
    args = parse_arguments()

    # Access the values of the arguments
    fasta_file = args.f
    output_file = args.o
    seed_kmer = args.i.upper()
    cutoff = args.c

    spacer = "NNN"

    logging.info(f"Load fasta file {fasta_file}")
    array, pos2header = load_fasta(fasta_file, spacer)
    logging.info(f"Find seed kmer {seed_kmer}")
    names_, positions_ = get_kmer_positions(array, seed_kmer)    
    logging.info(f"Build FS tree")
    fs_tree, abrupted_nodes = build_fs_tree_from_sequence(array, seed_kmer[0], names_, positions_, cutoff)
    logging.info(f"Build FS left tree")
    fs_left_tree, abrupted_left_nodes = build_fs_left_tree_from_sequence(array, seed_kmer[0], names_, positions_, cutoff)
    logging.info(f"Get loci")
    sequences, pair_sequences = get_loci(abrupted_left_nodes, abrupted_nodes, array, names_)
    logging.info(f"Join overlapping loci")
    joined_sequences = join_overlapping_loci(sequences, array)
    logging.info(f"Save loci")
    save_loci(joined_sequences, pos2header, output_file)


if __name__ == '__main__':
    main()