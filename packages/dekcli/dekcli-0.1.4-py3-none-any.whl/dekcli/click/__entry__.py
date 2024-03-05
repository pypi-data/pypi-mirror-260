from . import app
from .gitea import app as gitea_app

app.add_typer(gitea_app, name='gitea')


def main():
    app()
