import subprocess
import os

def list_files(startpath):
    if os.path.exists('/bin/tree'):
        subprocess.run(f'/bin/tree {startpath}', shell=True)
        return

    for root, _, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 2 * (level)
        if '.git' in root:
            continue
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 2 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
