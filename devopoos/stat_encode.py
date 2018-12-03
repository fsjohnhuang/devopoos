import os
import argparse
import cchardet
from devopoos.util import stringify_texttable
from devopoos.util.fn import F, rfind


def filter_subfiles(dir, ignore, root=None):
    filepaths = []
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if not ignore(path.replace(dir if root == None else root, '')):
            if os.path.isfile(path):
                filepaths.append(path)
            else:
                filepaths += filter_subfiles(path, ignore, dir if root == None else root)
            
    return filepaths


def get_encoding(filepath):
    with open(filepath, "rb") as fp:
        return cchardet.detect(fp.read())["encoding"]


def get_files_encoding(filepaths):
    return [(filepath, get_encoding(filepath)) for filepath in filepaths]


def get_subfiles_encoding(dir, ignore):
    ignore = F if ignore == None or ignore.strip() == '' else rfind(ignore)
    filepaths = filter_subfiles(dir, ignore)

    encodings = get_files_encoding(filepaths)
    return encodings


def print_subfiles_encoding(dir, ignore):
    str_encodings = stringify_texttable(get_subfiles_encoding(dir, ignore))
    print(str_encodings)


def get_encoding_unmatch_files(dir, ignore, encodings):
    files = []
    encodings = [encoding.lower() for encoding in encodings]
    for file, encoding in get_subfiles_encoding(dir, ignore):
        if not encodings.count(encoding.lower()):
            files.append((file, encoding))

    return files


def _argparse():
    parser = argparse.ArgumentParser(description='Welcome to use devopoos!')
    parser.add_argument('src')
    parser.add_argument('--ignore', dest='ignore')
    parser.add_argument('--encodings', dest='encodings')

    return parser.parse_args()


def main(config):
    parser = _argparse()

    src = parser.src
    ignore = parser.ignore
    if parser.encodings:
        encodings = [encoding.strip() for encoding in parser.encodings.split(',')]
        files = get_encoding_unmatch_files(src, ignore, encodings)
        print(stringify_texttable(files))
    else:
        print_subfiles_encoding(src, ignore)
