import os

def list_dirs(path):
    dirs = []
    for s in os.scandir(path):
        if s.is_dir():
            dirs.append(s)
            return dirs
        