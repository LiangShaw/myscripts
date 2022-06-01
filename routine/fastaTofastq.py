#!bin/bash
import sys
fasta = sys.stdin
row = fasta.readline()
while row:
    if row.startswith('>'):
        print('@'+row[1:].strip())
        seq = fasta.readline().strip()
        print(seq)
        print('+')
        print(''.join(['F' for _ in range(len(seq))]))
        row = fasta.readline()
    else:
        print('first line does not start with ">"')
        sys.exit()
