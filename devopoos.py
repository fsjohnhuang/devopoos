# -*- coding: utf-8 -*-
import sys
import logging
import argparse
from config import Config
from devopoos import cmpfiles
from devopoos import cmpfile
from devopoos import win_acl
from devopoos import stat_encode

logging.basicConfig(
    level=logging.WARN, format='%(asctime)s : %(levelname)s : %(message)s')


def _command_parser():
    parser = argparse.ArgumentParser(description='Welcome to use devopoos!')
    parser.add_argument('command', choices=['cmpfiles', 'cmpfile', 'stat_encode', 'win_acl'])

    return parser.parse_args()


def main():
    # 提起子命令
    argv = sys.argv
    if len(argv) > 1:
        sys.argv = argv[0:2]

    parser = _command_parser()
    cmd = parser.command

    # 执行子命令
    config = Config()
    sys.argv = argv[0:1] + argv[2:]
    if 'cmpfiles' == cmd:
        cmpfiles.main(config)
    elif 'cmpfile' == cmd:
        cmpfile.main(config)
    elif 'win_acl' == cmd:
        win_acl.main(config)
    elif 'stat_encode' == cmd:
        stat_encode.main(config)

if '__main__' == __name__:
    main()
