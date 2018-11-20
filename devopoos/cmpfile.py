import argparse
import os

from devopoos.util import gen_file_md5


def _argparser():
    parser = argparse.ArgumentParser(description='Welcome to use devopoos!')
    parser.add_argument('src')
    parser.add_argument('-d', dest='dst')
    parser.add_argument(
        '--mtime', action='store_true', dest='boolean_mtime', default=False)

    return parser.parse_args()


def main(config):
    parser = _argparser()

    if parser.dst:
        src_md5 = parser.src
        if os.path.isfile(parser.src):
            src_md5 = gen_file_md5(parser.src)

            if parser.boolean_mtime:
                src_md5 = "{}{}".format(src_md5, os.path.getmtime(parser.src))

        dst_md5 = parser.dst
        if os.path.isfile(parser.dst):
            dst_md5 = gen_file_md5(parser.dst)

            if parser.boolean_mtime:
                dst_md5 = "{}{}".format(dst_md5, os.path.getmtime(parser.dst))

        print('0' if src_md5 == dst_md5 else '1')
    else:
        print("{}{}".format(gen_file_md5(parser.src), os.path.getmtime(
            parser.src) if parser.boolean_mtime else ""))
