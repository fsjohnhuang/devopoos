import argparse
from os.path import isfile

from devopoos.util import gen_file_md5

def cmp_md5s(src, dst):
    src_md5 = gen_file_md5(src) if isfile(src) else src
    dst_md5 = gen_file_md5(dst) if isfile(dst) else dst

    return '0' if src_md5 == dst_md5 else '1'


def _argparser():
    parser = argparse.ArgumentParser(description='Welcome to use devopoos!')
    parser.add_argument('src')
    parser.add_argument('-d', dest='dst')

    return parser.parse_args()


def main(config):
    parser = _argparser()

    output = None
    src = parser.src
    if parser.dst:
        output = cmp_md5s(src, parser.dst)
    else:
        output = gen_file_md5(src)

    print(output)
