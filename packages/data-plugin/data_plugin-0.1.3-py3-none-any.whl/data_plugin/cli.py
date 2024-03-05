import typer

cli = typer.Typer()


@cli.command()
def say_hello(name: str):
    """Greet a person by name."""
    typer.echo(f"Hello, {name}!")


if __name__ == "__main__":
    cli()
