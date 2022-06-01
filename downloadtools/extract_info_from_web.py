###########################################
# 2021.12.14
# Shao-Bo Liang
# stop implementation...
###########################################
import os,argparse
import sys

def extract_info(web,thread,signal):
    information = os.popen(f"curl {web} | grep -P {signal} | head -n 1 | awk 'BEGIN{FS=\"\\\"\"}{printf $2}'").read()
    return information

def parser_webList(webFile,signal,threadN):
    webList = os.popen('cut -f 1 %s'%webFile).readlines()
    webList = [web.strip() for web in webList if not sra.startswith('#') ]
    for web in webList:
        information = extract_info(web, threadN, signal)

def main():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sra_file", \
        help="provide a input file.\n One SRA/SRX id per line", \
        type=str)  ## str or int.str default
    # optional arguments
    parser.add_argument("-o","--output", \
        help="specify a output directory.Default ./",
        default='./')
    parser.add_argument("-t","--thread", \
        help="thread number for download", \
        type=int, \
        default=1)
    parser.add_argument("-s","--signal", \
        help="key string for capturing infortation from web link.",
        type=str)
    parser.add_argument("-v","--verbose", \
        help="increase output verbosity", \
        action="store_true")
    args = parser.parse_args()
    sraFile = args.sra_file
    threadN = args.thread
    signal = args.signal

    parser_sraList(sraFile,signal,threadN)