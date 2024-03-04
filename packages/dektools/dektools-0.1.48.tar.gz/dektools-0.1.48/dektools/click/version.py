import sys
import typer
from ..version import version_digits

app = typer.Typer(add_completion=False)


@app.command()
def digits(version):
    sys.stdout.write(version_digits(version))
