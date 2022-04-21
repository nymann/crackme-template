import typer

app = typer.Typer()


@app.command()
def keygen() -> None:
    typer.echo("Implement your keygen for {{cookiecutter.project_slug}} here.")


if __name__ == "__main__":
    app()
