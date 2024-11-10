import click
import sqlalchemy
from quart import Quart

from .db_schema import metadata

DEFAULT_URL = "postgresql+psycopg://postgres:password@localhost/svr"
DB_URL_HELP = f"The URL for connecting to the database. Default: {DEFAULT_URL}"


def init_app(app: Quart) -> Quart:
    @click.option(
        "--db-url", default=DEFAULT_URL, envvar='CLI_DB_URL', help=DB_URL_HELP
    )
    @app.cli.command("initdb")
    def initdb(db_url):
        """ Initialize database. """
        click.echo("Initializing the database...", nl=False)
        engine = sqlalchemy.create_engine(db_url)
        metadata.drop_all(engine)
        metadata.create_all(engine)
        click.echo("done.")

    return app
