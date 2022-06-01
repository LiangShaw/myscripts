###########################################
# 2020.7.28
# ShawLiang
# download SRA data using command 'lftp'
###########################################
import os,argparse
import sys

def GSM_to_SRX(GSM):
    SRXs = os.popen(f"curl https://www.ncbi.nlm.nih.gov/sra/?term={GSM} | grep -P 'SRX[0-9]+' -o ").readlines()
    SRXs = { SRX.strip() for SRX in SRXs }
    return SRXs

def SRX_to_SRA(SRX):
    SRAs = os.popen(f"curl https://www.ncbi.nlm.nih.gov/sra/?term={SRX} | grep -P 'SRR[0-9]+' -o ").readlines()
    SRAs = { sra.strip() for sra in SRAs }
    return SRAs

def download(sra_no,thread,signal):
    # singal: "sra-pub-src" "\'<td><a href=\"https://sra-pub-\'" ever used
    https = os.popen("curl https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=%s | grep %s | \
        awk 'BEGIN{FS=\"\\\"\"}{print $2}'"%(sra_no,signal)).readlines()
    if https:
        for http in https:
            os.system('lftp -e \'pget -n {} -c \"{}\";exit\''.format(thread,http.strip()))
    else:
        print("The web does not exist")
        sys.exit(1)

def parser_sraList(sraFile,singal):
    sraList = os.popen('cut -f 1 %s'%sraFile).readlines()
    #if not sraList[-1].startswith('RR',1,3):
    #    sraList.pop()
    #else:pass
    sraList = [sra for sra in sraList if sra[1]=='R' and sra[0]!='#']
    # should collect all SRAs, while it's not common. If necessary, i will implement
    sraList = [sra.strip() if sra.startswith('RR',1,3) else SRX_to_SRA(sra.strip())[0]  for sra in sraList]

    for sra in sraList:
        sra = sra.split('\t')[0]
        if sra.startswith('#'):
            continue
        sra = sra.split('\t')[0]
        download(sra,threadN,signal)

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
        help="key string for capturing web link.Default 'sra-download'.",
        type=str,
        default="sra-download")
    parser.add_argument("-v","--verbose", \
        help="increase output verbosity", \
        action="store_true")
    args = parser.parse_args()
    sraFile = args.sra_file
    threadN = args.thread
    signal = args.signal

    parser_sraList(sraFile,signal)
