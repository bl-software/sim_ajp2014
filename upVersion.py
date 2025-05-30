#!/usr/bin/env python

import datetime
from VERSION import version
import subprocess

githash=subprocess.check_output(['git', 'rev-parse', 'HEAD'], encoding='utf8').strip()
print(f'githash=###{githash}### t:{type(githash)}')
nowstr=datetime.datetime.now().strftime('%Y-%m-%d:%H%M%S')

EXAMPLEversion= '2.0.0 GIT(HEAD-1):c83d12b4462a31f0a32c00012300470b05ac7645 DATE:2018-08-22:183140'

def update():
    v,g,d= version.split(' ')
    major, minor, build = v.split('.')

    newv= f'{major}.{minor}.{int(build)+1} GIT(HEAD-1):{githash} DATE:{nowstr}'
    print('newv=',newv)
    with open('VERSION.py', 'w') as f:
        f.write(f"version='{newv}'\n")

    print( f'New Version=:{subprocess.check_output(["cat", "VERSION.py"], encoding="utf8").strip()}' )

    retval= subprocess.check_output(["git", "add", "VERSION.py"], encoding='utf8').strip()
    print( 'retval of git add: %s'%retval )
    if retval:
        return retval
    else:
        return 0

if __name__=='__main__':
    update()
