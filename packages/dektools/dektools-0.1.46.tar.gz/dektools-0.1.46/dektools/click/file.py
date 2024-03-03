import os
import glob
import typer
from ..file import normal_path, write_file, remove_path, merge_assign, FileHitChecker
from ..shell import shell_wrapper
from ..typer import command_mixin

app = typer.Typer(add_completion=False)


@app.command()
def remove(path, ignore='.rmignore'):
    def walk(fp, is_hit, _):
        if not is_hit:
            remove_path(fp)

    path = normal_path(path)
    if os.path.isdir(path):
        FileHitChecker(path, ignore).walk(walk)
    elif os.path.isfile(path):
        if not FileHitChecker(os.path.dirname(path), ignore).is_hit(path):
            remove_path(path)


@app.command()
def merge(dest, src, ignore=None):
    def walk(fp, is_hit, rp):
        if not is_hit:
            write_file(os.path.join(dest, rp), c=fp)

    if ignore:
        FileHitChecker(src, ignore).walk(walk)
    else:
        merge_assign(dest, src)


@app.command()
def remove(filepath):
    remove_path(filepath)


@app.command()
def write(
        filepath,
        s=None, b=None, sb=None,
        m=None, mi=None,
        c=None, ci=None,
        ma=None, mo=None,
        t=False,
        encoding='utf-8'):
    write_file(
        filepath,
        s=s, b=b, sb=sb,
        m=m, mi=mi,
        c=c, ci=ci,
        ma=ma, mo=mo,
        t=t,
        encoding=encoding
    )


@command_mixin(app, name='glob')
def glob_(args, path):
    result = glob.glob(path, recursive=True)
    if result:
        shell_wrapper(args.format(filepath=result[-1]))


@command_mixin(app)
def globs(args, path):
    result = glob.glob(path, recursive=True)
    for file in result:
        shell_wrapper(args.format(filepath=file))
