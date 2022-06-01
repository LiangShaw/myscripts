import os
import sys
import argparse
import time

def splitfile(filepath,input_file=True,linesize=10000,verbose=False):
    print('Start to split %s...'%filepath)
    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)
    filedir = os.path.join(filedir,name)
    if not os.path.exists(filedir):
        os.mkdir(filedir)
         
    partno = 0
    if input_file:
        stream = open(filepath,'r', encoding='utf-8')
    else:stream = sys.stdin
    while True:
        partfilename = os.path.join(filedir,name + '_' + str(partno) + ext)
        if verbose:
            print('write start %s' % partfilename)
        part_stream = open(partfilename,'w', encoding='utf-8')
 
        read_count = 0
        while read_count < linesize:
            read_content = stream.readline()
            if read_content:
                part_stream.write(read_content)
            else:
                break
            read_count += 1
          
        part_stream.close()
        if(read_count < linesize) :
            break
        partno += 1
    print('into %d files'%(partno+1))
    
def make_parser():
    parser = argparse.ArgumentParser(
        description='splitfile.py script is used to split big file '
        'into several small files for following parallel treatments.'
        'Specify "-" to gain pipeline output, which mainly takes bam transformation into consideration.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    req_parse_grp = parser.add_argument_group(
        title='required arguments (-f, -l)'
    )
    req_parse_grp.add_argument(
        '-f',
        '--filename',
        help='directory of bigfile to split. If "-" is specified, '
        'stdin is as input.'
    )
    req_parse_grp.add_argument(
        '-l',
        '--linenumber',
        type=int,
        help='split *l* lines in every samll file'
    )
    parser.add_argument(
        '-o',
        '--prefix',
        type=str,
        default='./split',
        help='prefix of the output files'
    )
    parser.add_argument(
        '-s',
        '--suffix',
        type=str,
        default='.sam',
        help='suffix/type of input file'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        choices=[True,False],
        default=False,
        help='print split process information'
    )
    
    return parser

def spendtime(start_time,end_time):
    seconds = end_time - start_time
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return '%d h: %d min: %d sec'%(hours,minutes,seconds)
    
if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    # parse parameters
    filename = args.filename
    linenum = args.linenumber
    prefix = args.prefix
    suffix = args.suffix
    v = args.verbose
    start_time = time.time()
    if filename=='-':
        filename = prefix+suffix
        splitfile(filename,input_file=False,linesize=linenum,verbose=v)
    else:
        splitfile(filename,linesize=linenum,verbose=v)
    end_time = time.time()
    cost_time = end_time - start_time
    print('Split task Done.\nTime used %s seconds'%cost_time)