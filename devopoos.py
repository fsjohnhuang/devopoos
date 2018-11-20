# -*- coding: utf-8 -*-
import sys
import argparse
from config import Config
from devopoos import cmpfiles


def _command_parser():
    parser = argparse.ArgumentParser(description='Welcome to use devopoos!')
    parser.add_argument('command', choices=['cmpfiles'])

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


if '__main__' == __name__:
    main()
