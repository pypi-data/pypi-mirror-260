import shutil
import time
from pathlib import Path

import typer

from f1_fantasy.consts import ROOT_DIR, CURRENT_DIR
from f1_fantasy.main import drivers_prices_from_csv, constructors_prices_from_csv, finishing_positions_from_csv, \
    special_points_from_csv, set_chips_from_csv, calculations

app = typer.Typer()


@app.command()
def setup():
    current_dir = Path() / "data"
    typer.echo(f"Copying data to {current_dir}")
    shutil.copytree(ROOT_DIR / "data", current_dir)


@app.command()
def run():
    if Path(CURRENT_DIR / "data" / "input" / "prices_drivers.csv").exists() is False:
        typer.echo("No input data found. Run setup command first: f1-fantasy setup")
        return

    driver_prices = drivers_prices_from_csv(Path(CURRENT_DIR / "data" / "input" / "prices_drivers.csv"))
    constructor_prices = constructors_prices_from_csv(Path(CURRENT_DIR / "data" / "input" / "prices_constructors.csv"))
    qualifying_finishing_positions = finishing_positions_from_csv(
        Path(CURRENT_DIR / "data" / "input" / "qualifying_finishing_positions.csv")
    )
    racing_finishing_positions = finishing_positions_from_csv(
        Path(CURRENT_DIR / "data" / "input" / "race_finishing_positions.csv")
    )
    special_points = special_points_from_csv(Path(CURRENT_DIR / "data" / "input" / "special_points.csv"))
    set_chips_from_csv(Path(CURRENT_DIR / "data" / "input" / "chips.csv"))

    _max_score_teams = calculations(
        driver_prices=driver_prices,
        constructor_prices=constructor_prices,
        qualifying_finishing_positions=qualifying_finishing_positions,
        racing_finishing_positions=racing_finishing_positions,
        special_points=special_points,
    )
    output_file = Path(CURRENT_DIR / "data" / "output" / f"{int(time.time())}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w+") as f:
        for team in _max_score_teams:
            print(team)
            f.write(f"{team}\n")
        f.write(str(len(_max_score_teams)))
        print(len(_max_score_teams))


def version_callback(value: bool):
    import pkg_resources

    my_version = pkg_resources.get_distribution('f1-fantasy').version
    if value:
        typer.echo(f"{my_version}")
        raise typer.Exit()


@app.callback()
def cli(
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
):
    return


if __name__ == "__main__":
    app()
