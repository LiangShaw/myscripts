###########################################
# 2020.7.28
# ShawLiang
# download SRA data using command 'lftp'
###########################################
import os,argparse
import sys

def SRX_to_SRA(SRX):
    sra = os.popen("curl https://www.ncbi.nlm.nih.gov/sra/?term=%s | grep -P 'SRR[0-9]+' -o "%SRX).readlines()[-1].strip()
    return sra

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

def parser_sraList(sraFile):
    sraList = os.popen('cut -f 1 %s'%sraFile).readlines()
    if not sraList[-1].startswith('S'):
        sraList.pop()
    else:pass

    sraList = [sra.strip() if sra.startswith('SRR') else SRX_to_SRA(sra.strip())  for sra in sraList]
    for sra in sraList:
        sys.stdout.write(sra+'\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sra_file", \
        help="provide a input file.\n One SRA/SRX id per line", \
        type=str)  ## str or int.str defaul
    args = parser.parse_args()
    sraFile = args.sra_file

    parser_sraList(sraFile)
