import typer
from loguru import logger

cli = typer.Typer(no_args_is_help=True)


@cli.command()
def hello():
    print("this is an hello from co2_cli_template")
    logger.error("here")
