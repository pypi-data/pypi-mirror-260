import os
import sys
import shutil
from dektools.sys import sys_paths_relative

shell_name = __name__.split(".", 1)[0]


def search_bin_by_path_tree(filepath, bin_name):
    filepath = os.path.normpath(os.path.abspath(filepath))
    cursor = os.path.dirname(filepath) if os.path.isfile(filepath) else filepath
    while True:
        for venv_name in ('venv', 'env', '.venv'):
            path_venv = os.path.join(cursor, venv_name)
            if os.path.isdir(path_venv):
                if sys.prefix == path_venv:
                    return
                else:
                    path_scripts = sys_paths_relative(path_venv)['scripts']
                    path_exe = shutil.which(bin_name, path=path_scripts)
                    if path_exe:
                        return path_exe
        dir_cursor = os.path.dirname(cursor)
        if dir_cursor == cursor:
            break
        cursor = dir_cursor


def redirect_shell_by_path_tree(filepath):
    return search_bin_by_path_tree(filepath, shell_name)
