import os,sys
import argparse

parser = argparse.ArgumentParser(usage='merge one column information depending on the same another column names.')
parser.add_argument('input',type=str, help='file name or - for stdin')
parser.add_argument('-o','--output',type=str,help='output file. Default stdout')
parser.add_argument('-a','--depend-column',default=1,type=int,help='number of depending column. Default 1st column')
parser.add_argument('-b','--merge-column',default=2,type=int,help='number of column to merge. Default 2st column')
parser.add_argument('-s','--input-sep',default='\t', type=str,help='set input separator')
parser.add_argument('--output-sep',default='\t', type=str,help='set output separator')
parser.add_argument('--merge-separator',default=',',type=str,help='set separator for merge. Default comma')

args_dict = vars(parser.parse_args())

d_col = args_dict['depend_column']
m_col = args_dict['merge_column']
m_sep = args_dict['merge_separator']
i_sep = args_dict['input_sep']

sys.stderr.write('Note: please sort the depending column first by yourself!\n')

if args_dict['input'] == '-':
    input_content = sys.stdin
else:
    input_content = open(args_dict['input'],'r')

first_line_ls = input_content.readline().strip().split(i_sep)
name_p = first_line_ls[d_col-1]
merge_p = first_line_ls[m_col-1]

if args_dict['output']:
    with open(args_dict['output'],'w') as fo:
        for line in input_content:
            line_ls = line.strip().split(i_sep)
            name = line_ls[d_col-1 ]
            info = line_ls[m_col-1]
            if name_p != name:
                fo.write(name_p + args_dict['output_sep'] + merge_p)
                merge_p = info
                name_p = name
            else:
                merge_p += m_sep + info
        # last record
        fo.write(name_p + args_dict['output_sep'] + merge_p)
else:
    # stdout
    for line in input_content:
        line_ls = line.strip().split(i_sep)
        name = line_ls[d_col-1 ]
        info = line_ls[m_col-1]
        if name_p != name:
            sys.stdout.write(name_p + args_dict['output_sep'] + merge_p + '\n')
            merge_p = info
            name_p = name
        else:
            merge_p += m_sep + info
    # last record
    sys.stdout.write(name_p + args_dict['output_sep'] + merge_p + '\n')