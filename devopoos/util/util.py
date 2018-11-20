import hashlib
import os

from devopoos.util.fn import F


def gen_file_md5(filepath):
    """Returns md5 string of the indicated file
    """
    size = 8024
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        chunck = f.read(size)
        while chunck:
            md5.update(chunck)
            chunck = f.read(size)

    str_md5 = md5.hexdigest()
    return str_md5


def gen_files_md5(dir, ignore=F):
    """Returns pairs consist of filepath and md5 string
    """
    files_md5 = []
    for curr_dir, _, filenames in os.walk(dir):
        for filename in filenames:
            if not ignore(filename):
                filepath = os.path.join(curr_dir, filename)
                files_md5.append((filepath, gen_file_md5(filepath)))

    return files_md5


def gen_files_md5(path, ignore=F, mtime=False):
    """Returns pairs consist of filepath and md5 string
    """
    if not os.path.exists(path):
        raise Exception("{} is not an available path.".format(path))

    md5s = []
    if os.path.isfile(path):
        md5s.append((path, gen_file_md5(path)))
    else:
        md5s = gen_files_md5(path, ignore)

    if mtime:
        md5s = map(lambda (filepath, md5): (filepath, "%s%s" %
                                            (md5, os.path.getmtime(filepath))), md5s)

    return md5s


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


# gen_files_md5("/home/john/playround/pymd5sum.py")
# stringify_texttable([(1, 2, 3), ("csdf", "xxoin")])
# parse_texttable("1 2 3\nxong ccc")
