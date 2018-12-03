import hashlib
import os

def gen_file_md5(filepath):
    size = 8024
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        chunck = f.read(size)
        while chunck:
            md5.update(chunck)
            chunck = f.read(size)

    str_md5 = md5.hexdigest()
    return str_md5


def _gen_file_md5_lst(filepaths):
    return [(filepath, gen_file_md5(filepath)) for filepath in filepaths]


def gen_file_md5_lst(filepaths, ignore):
    return _gen_file_md5_lst(
        [filepath for filepath in filepaths if not ignore(filepath)])


def gen_dir_md5(dir, ignore):
    filepaths = []
    for root, _, files in os.walk(dir):
        filepaths += [os.path.join(root, file) for file in files]

    return gen_file_md5_lst(filepaths, ignore)




def stringify_texttable(rows):
    lines = []
    for cols in rows:
        cols = map(str, cols)
        lines.append(' '.join(cols))

    return '\n'.join(lines)


def _parse_texttable(txt):
    rows = []
    for line in txt.strip().split('\n'):
        row = []
        for col in line.strip().split(' '):
            row.append(col.strip())

        rows.append(tuple(row))

    return rows


def parse_texttable(src):
    texttable = src
    if os.path.isfile(src):
        with open(src, 'r') as f:
            texttable = f.read()

    return _parse_texttable(texttable)
