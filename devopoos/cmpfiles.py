# -*- coding: utf-8 -*-
import logging
import argparse
from devopoos.util import (
    gen_dir_md5, stringify_texttable, parse_texttable
)
from devopoos.util.fn import rfind, F


def gen_subfiles_md5(dir, ignore):
    ignore = rfind(ignore) if ignore else F
    md5_list = gen_dir_md5(dir, ignore)
    md5_list = [(path.replace(dir, ''), md5) for path, md5 in md5_list]

    return md5_list


def cmp_md5(src_md5s, dst_md5s):
    logging.debug(src_md5s)
    results = []
    for s_path, s_md5 in src_md5s:
        status = 0  # 0 not found; 1 diff; 2 same
        for d_path, d_md5 in dst_md5s:
            if s_path == d_path:
                status = 2 if s_md5 == d_md5 else 1

            if status != 0:
                break

        results.append((status, s_path))

    return results


def print_dir_md5(dir, ignore):
    md5s = gen_subfiles_md5(dir, ignore)
    str_md5s = stringify_texttable(md5s)

    print(str_md5s)


def print_cmp_dir(src1, src2, ignore):
    src1_md5s = gen_subfiles_md5(src1, ignore)
    src2_md5s = gen_subfiles_md5(src2, ignore)
    cmp_results = cmp_md5(src1_md5s, src2_md5s)
    str_results = stringify_texttable(cmp_results)

    print(str_results)


def _argparse():
    parser = argparse.ArgumentParser(description='Welcome to use devopoos!')
    parser.add_argument('src')
    parser.add_argument('-d', dest='src2')
    parser.add_argument('--ignore', dest='ignore')

    return parser.parse_args()


def main(config):
    """
    cmpfiles '/directory'
    cmpfiles '/filepath' -d '/destination/directory'
    """
    parser = _argparse()

    src = parser.src
    src2 = parser.src2
    ignore = parser.ignore
    if src2:
        print_cmp_dir(src, src2, ignore)
    else:
        print_dir_md5(src, ignore)
    
