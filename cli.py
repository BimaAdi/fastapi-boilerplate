import re
import sys
import typer
import seed.seed_runner

app = typer.Typer()

@app.command()
def list_seed():
    """
    show all function inside seed.seed_runner.py\n
    you can add/remove seed by edit seed.seed_runner.py
    """
    for item in dir(seed.seed_runner):
        if not re.search('^__.*__$', item):
            typer.echo(f'- {item}')

@app.command()
def run_seed(func_name:str):
    """
    Run seeder function inside seed.seed_runner.py\n
    you can add/remove seed by edit seed.seed_runner.py
    """
    try:
        method_to_call = getattr(seed.seed_runner, func_name)
        method_to_call()
    except Exception as e:
        typer.echo(str(e))

@app.command()
def show_python_version():
    """
    show python version used

    """
    typer.echo(sys.version)

if __name__ == "__main__":
    app()
