"""
Скрипт для управления дистрибутивом aud_alert_tg_bot
"""
import sys
from argparse import ArgumentParser
from os import path
from pathlib import Path
from zipfile import ZipFile

FOR_ZIP_DIRNAMES = ['tg_bot', 'command']
FOR_ZIP_FILENAMES = ['README.md', 'LICENSE', 'empty.env', 'requirements.txt', 'run_app.bat', 'run_app.sh']


def parse_args(args):
    parser = ArgumentParser(prog='python manage.py',
                            description=''.join(('Скрипт для управления дистрибутивом скрипта aud_alert_tg_bot')),
                            epilog='(c) 2025')

    parser.add_argument('-m', '--makezip', metavar='{file}', help='Создание архива для передачи пользователям')
    return parser.parse_args(args)


def _get_all_zip_files(rootdirname, dirname):
    zip_files = []
    for _root, _dirs, _files in dirname.walk(top_down=True):
        if not str(_root).startswith('_') and not str(_root).endswith('_'):
            for name in _files:
                zip_files += [path.join(rootdirname, _root, name)]
    return zip_files


def _get_zip_files(dirname):
    zip_files = []
    for _root, _dirs, _files in dirname.walk(top_down=True):
        if _root.name == '':
            for name in [n for n in _dirs if n in FOR_ZIP_DIRNAMES]:
                zip_files += _get_all_zip_files(_root, Path(name))
            for name in [n for n in _files if n in FOR_ZIP_FILENAMES]:
                zip_files += [path.join(_root, name)]
    return zip_files


def make_zip_file(filename: str):
    zip_files = _get_zip_files(Path('.'))
    with ZipFile(filename if filename.endswith('.zip') else filename, 'w') as zip_object:
        for file in zip_files:
            zip_object.write(file, file)


# загрузка указанных параметров запуска модуля
args = parse_args(sys.argv[1:])

if args.makezip:
    make_zip_file(args.makezip)
