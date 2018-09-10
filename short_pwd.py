#!/usr/bin/env python3
import os
from socket import gethostname
from subprocess import run, PIPE
import re

def escaper(b, e, content):
    return '\\[\x1b[{}m\\]{}\\[\x1b[{}m\\]'.format(b, content, e)
def int_or_none(s):
    try: return int(s) 
    except: return None

trunc_len = int_or_none(os.environ.get('PROMPT_TRUNCATE_LENGTH')) or 20
path_len = int_or_none(os.environ.get('PROMPT_PATH_LENGTH')) or 5

hostname = gethostname()
username = os.environ['USER']
pwd = os.getcwd()
homedir = os.path.expanduser('~')
pwd = pwd.replace(homedir, '~', 1)
if len(pwd) > trunc_len:
    # pwd = '\[\x1b[31m/\x1b[0m\]'.join(list(map(lambda x: x[0:4] if len(x) > 0 else '', pwd.split('/'))))
    pwd = escaper(
        31, 0, '/').join(list(map(lambda x: x[0:path_len] if len(x) > path_len else x, pwd.split('/'))))
    pwd += escaper(31, 0, '/')
    # pwd = pwd[:10]+'...'+pwd[-20:] # first 10 chars+last 20 chars

branch = ''
if run(['which', 'git'], stderr=PIPE, stdout=PIPE).returncode is 0:
    g_branch = run(['git', 'branch'], stderr=PIPE, stdout=PIPE)
    if g_branch.returncode is not 0 or len(g_branch.stdout) < 1:
        pass
    else:
        changed = ''
        if len(run(['git', 'status', '-s'], stdout=PIPE, stderr=PIPE).stdout) > 1:
            changed = escaper(35, 0, '*')
        s = g_branch.stdout.decode('utf-8')
        branch = escaper(36, 0, ' ({}').format(
            re.search(r'^\*\s+(.+)$', s, re.MULTILINE).group(1), changed)
        branch += changed
        branch += escaper(36, 0, ')')

print('{}@{}:{}{} '.format(username, hostname, pwd, branch))