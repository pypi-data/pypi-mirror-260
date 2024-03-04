import shutil
from pathlib import Path

import typer
from f1_fantasy.main import main
from f1_fantasy.consts import ROOT_DIR

app = typer.Typer()


@app.command()
def setup():
    shutil.copytree(ROOT_DIR / "data", Path())


@app.command()
def run():
    main()



if __name__ == "__main__":
    app()
