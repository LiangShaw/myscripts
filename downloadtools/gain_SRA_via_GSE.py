#!/usr/bin/env python

import sys, os

def get_SRA_from_GSE(GSE):
    SRA = os.popen('curl https://www.ncbi.nlm.nih.gov/sra/?term=%s  | grep -P \'SRR[0-9]*\' -o'%(GSE)).readline()
    return SRA

def main(file):
    GSEs = [ gse.strip() for gse in sys.stdin.readlines()]
    with open(file, 'w') as fo:
        for gse in GSEs:
            SRA = get_SRA_from_GSE(gse)
            fo.write(gse + "\t" + SRA.strip() + "\n")

if __name__ == '__main__':
    main(sys.argv[1])
