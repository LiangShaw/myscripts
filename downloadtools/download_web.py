#####################
# 2021.10.21
# ShawLiang
# download data using command lftp via web page link
#####################

import os, sys
import argparse
import pandas as pd

def download(web,thread, name=False):
    if name:
        os.system(f'lftp -e \'pget -n {thread} -c \"{web}\" -o {name};exit\'')
    else:
        os.system(f'lftp -e \'pget -n {thread} -c \"{web}\";exit\'')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='Quickly download large files via lftp. Make sure lftp command available')
    parser.add_argument("-a","--web-address",
        help="web link to download",nargs="+",
        type=str)

    parser.add_argument("-f", "--address-file",
        help="provide a file containing two columns: target and web links, titled by 'web' and 'name' respectively",
        type=str)

    parser.add_argument("-t", "--thread",
        help="thread number for download",
        type=int,
        default=1)

    #web_list = list()
    args = parser.parse_args()
    threadN = args.thread

    try:
        for web in args.web_address:
            download(web, threadN)
    except:
        pass

    try:
        web_file = args.address_file
        web_table = pd.read_table(web_file, header=0, sep='\t')
        web_links = list(web_table['web'])
        for web, name in zip(web_table['web'], web_table['name']):
            download(web, threadN, name)
    except:pass