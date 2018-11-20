# -*- coding: utf-8 -*-
# 通过MD5+mtime比较两个目录的的文件内容
import os
import logging
import argparse
from devopoos.util import gen_files_md5, stringify_texttable, parse_texttable
from devopoos.util.fn import rfind, complement, F


def gen_md5_list(dir, ignore, mtime):
    ignore = rfind(ignore) if ignore else F
    md5_list = gen_files_md5(dir, ignore, mtime)
    md5_list = [(item[0].replace(dir, ''), item[1]) for item in md5_list]
    logging.debug(md5_list)

    return md5_list


def cmp_md5(src_md5s, dst_md5s):
    logging.debug(src_md5s)
    results = []
    for src_md5 in src_md5s:
        s_path, s_md5 = src_md5
        status = 0  # 0 not found; 1 diff; 2 same
        for d_path, d_md5 in dst_md5s:
            if s_path == d_path:
                status = 2 if s_md5 == d_md5 else 1

            if status != 0:
                break

        results.append((status,) + src_md5)

    return results


def cmp_md5_dir(src_md5s, dst, ignore, mtime):
    dst_md5s = gen_md5_list(dst, ignore, mtime)
    return cmp_md5(src_md5s, dst_md5s)


def cmp_dirs(src, dst, ignore, mtime):
    src_md5s = gen_md5_list(src, ignore, mtime)
    dst_md5s = gen_md5_list(dst, ignore, mtime)
    return cmp_md5(src_md5s, dst_md5s)


def gen_cmp_dirs_str(src, dst, ignore, mtime):
    result = cmp_dirs(src, dst, ignore, mtime)
    str_result = stringify_texttable(result)

    print(str_result)


def gen_files_md5_str(dir, ignore, mtime):
    md5s = gen_md5_list(dir, ignore, mtime)
    str_md5s = stringify_texttable(md5s)

    print(str_md5s)


def _argparse():
    parser = argparse.ArgumentParser(description='Welcome to use devopoos!')
    parser.add_argument(
        'src', help='Source directory path or file path contains file path and md5 string pairs.')
    parser.add_argument(
        '-d', dest='dst', help='Destination directory path or file path contains file path and md5 string pairs.')
    parser.add_argument(
        '--ignore', dest='ignore')
    parser.add_argument(
        '--mtime', action='store_true', dest='boolean_switch', default=False)

    return parser.parse_args()


def main(config):
    """
    cmpfiles '/directory'
    cmpfiles '/filepath' -d '/destination/directory'
    """
    parser = _argparse()

    if not parser.dst:
        gen_files_md5_str(parser.src, parser.ignore, parser.boolean_switch)
    else:
        if os.path.isfile(parser.src):
            md5s = ""
            with open(parser.src, 'r') as f:
                md5s = f.read()
            md5s = parse_texttable(md5s)
            results = cmp_md5_dir(
                md5s, parser.dst, parser.ignore, parser.boolean_switch)
            print(stringify_texttable(results))
        else:
            gen_cmp_dirs_str(parser.src, parser.dst,
                             parser.ignore, parser.boolean_switch)
