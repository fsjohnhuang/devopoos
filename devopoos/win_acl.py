# -*- coding: utf-8-*-
import re
import argparse
import subprocess
import os


def _extract_normal_perm(str_perm):
    r = "(?:\((IO|OI|CI|ID)\))?" * 4 + "(N|R|C|F)$"
    m = re.search(r, str_perm)
    if not m:
        return None, None

    groups = m.groups()
    perm = groups[4]
    methods = tuple([method for method in groups[0:4] if method])

    return methods, perm


def _extract_perm(path, lines):
    lines = [line for line in lines if line.strip()]

    fst_line = lines[0]
    lines = [fst_line.replace(path, '')] + lines[1:]

    acl = []
    account = None
    methods = None
    perm = None
    privilege = None
    str_perm = None
    for line in lines:
        line = line.strip()
        if line.count(':') > 0:
            if account:
                methods, perm = _extract_normal_perm(str_perm)
                if not perm:
                    privilege = str_perm

                acl.append((account, perm, methods, privilege))
                account = None
                methods = None
                perm = None
                privilege = None
                str_perm = None

            segs = line.split(':')
            account = segs[0]
            str_perm = ''.join(segs[1:])
        else:
            str_perm += line

    if account:
        methods, perm = _extract_normal_perm(str_perm)
        if not perm:
            privilege = str_perm

        acl.append((account, perm, methods, privilege))

    return tuple(acl)


# _extract_perm('C:\Users\john\Local Settings', s)


def check_acl(path):
    """返回目录/文件的ACL
    Returns ((帐号, 普通权限, 获取方式, 特殊权限))
    """
    proc = subprocess.Popen('cacls {}'.format(
        path), shell=True, stdout=subprocess.PIPE)
    proc.wait()
    lines = proc.stdout.readlines()
    lines = [line.decode('gb2312') for line in lines]

    return _extract_perm(path, lines)


def check_acls(dirpath):
    """返回目录及其下子目录和文件的ACL
    Returns ((路径,((帐号, 普通权限, 获取方式, 特殊权限))))
    """
    acls = []
    for curr_dir, dirnames, filenames in os.walk(dirpath):
        paths = [os.path.join(curr_dir, dirname) for dirname in dirnames] + \
            [os.path.join(curr_dir, filename) for filename in filenames]
        acls += [(path, check_acl(path)) for path in paths]

    acls.append((dirpath, check_acl(dirpath)))
    return tuple(acls)


def sort_by_matched_or_not(path, user, perm):
    acls = None
    if os.path.isfile(path):
        acls = ((path, check_acl(path)))
    else:
        acls = check_acls(path)

    matches = []
    unmatches = []
    for filepath, acl in acls:
        found = False
        for account, normal_perm, _, _ in acl:
            if account == user and normal_perm == perm:
                found = True
                break
        if found:
            matches.append(filepath)
        else:
            unmatches.append(filepath)

    return matches, unmatches


def empower(path, user, perm):
    cmds = ["cacls {} /E /C /P {}:{}".format(
        path, user, perm), "cacls {} /T /E /C /P {}:{}".format(path, user, perm)]

    for cmd in cmds:
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()

    matched, unmatched = sort_by_matched_or_not(path, user, perm)
    return len(unmatched) == 0


def _argparse():
    parser = argparse.ArgumentParser(description='Welcome to use devopoos!')
    parser.add_argument('path')
    parser.add_argument('--user_perm', dest='user_perm')
    parser.add_argument('-a', dest="boolean_append",
                        action="store_true", default=False)

    return parser.parse_args()


def main(config):
    parser = _argparse()
    path = parser.path

    if not parser.user_perm:
        print(check_acl(path))
    else:
        if parser.boolean_append:
            print('0' if empower(path, *parser.user_perm.split(':')) else '1')
        else:
            matches, unmatches = sort_by_matched_or_not(
                path, *parser.user_perm.split(':'))
            print(unmatches)
