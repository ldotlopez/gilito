import logging

from .cli import cli

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger("gilito").setLevel(logging.DEBUG)

    cli()
