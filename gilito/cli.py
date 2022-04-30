import os

import click
import gilito
from gilito import PluginType
import gilito.models
import io


@click.group()
def cli():
    pass


@click.command(name="convert")
@click.option(
    "--file",
    required=True,
    help="Input filename (xlsx usually)",
    type=click.File(mode="rb", encoding=None, errors="strict", lazy=None, atomic=False),
)
@click.option(
    "--converter",
    required=False,
    help="Converter to use",
    type=str,
)
def convert_file_to_csv(file: io.BufferedReader, converter=None):
    if converter is None:
        _, ext = os.path.splitext(file.name)
        converter = ext[1:]

    conv = gilito.get_plugin(PluginType.IMPORTER, converter).Importer()

    print(conv.process(file.read()))


@click.command(name="map")
@click.option(
    "--file",
    required=True,
    help="CSV file to read",
    type=click.File(mode="rb", encoding=None, errors="strict", lazy=None, atomic=False),
)
@click.option(
    "--mapper",
    required=True,
    help="Rules to apply to use",
    type=str,
)
def map_csv_to_transactions(file, mapper):
    m = gilito.get_plugin(PluginType.MAPPER, mapper).Mapper()

    csvdata = file.read().decode("utf-8")
    logbook = m.map(csvdata)

    # cats = gilito.rules.categories.Categorization()
    # logbook = [cats.process(tr) for tr in transactions]

    print(logbook.json(indent=2))


@click.command(name="process")
@click.option(
    "--file",
    required=True,
    help="CSV file to read",
    type=click.File(mode="rb", encoding=None, errors="strict", lazy=None, atomic=False),
)
@click.option(
    "--processors",
    multiple=True,
    required=True,
    help="Rules to apply to use",
    type=str,
)
def process_logbook(file, processors):
    logbook = gilito.models.LogBook.parse_raw(file.read())
    processors = [
        gilito.get_plugin(PluginType.PROCESSOR, processor).Processor()
        for processor in processors
    ]

    for proc in processors:
        logbook = proc.process(logbook)

    print(logbook.json(indent=2))


opt_file = click.option(
    "--file",
    required=True,
    help="Input file",
    type=click.File(mode="rb", encoding=None, errors="strict", lazy=None, atomic=False),
)
opt_mapper = click.option(
    "--mapper",
    required=False,
    help="Rules to apply to use",
    type=str,
)
opt_processors = click.option(
    "--processors",
    multiple=True,
    required=True,
    help="Rules to apply to use",
    type=str,
)
opt_converter = click.option(
    "--converter",
    required=False,
    help="Converter to use",
    type=str,
)


@click.command(name="run")
@opt_file
@opt_converter
@opt_mapper
@opt_processors
def run(file, converter, mapper, processors):
    data = file.read()

    if converter:
        Importer = gilito.get_plugin(PluginType.IMPORTER, converter).Importer
        data = Importer().convert(data)

    if mapper:
        Mapper = gilito.get_plugin(PluginType.MAPPER, mapper).Mapper
        data = Mapper().map(data)

    if processors:
        for proc in processors:
            Processor = gilito.get_plugin(PluginType.PROCESSOR, proc).Processor
            data = Processor.process(data)

    m = gilito.get_plugin(PluginType.MAPPER, mapper).Mapper()

    csvdata = file.read().decode("utf-8")
    logbook = m.map(csvdata)

    # cats = gilito.rules.categories.Categorization()
    # logbook = [cats.process(tr) for tr in transactions]

    print(logbook.json(indent=2))


cli.add_command(convert_file_to_csv)
cli.add_command(map_csv_to_transactions)
cli.add_command(process_logbook)
cli.add_command(run)


if __name__ == "__main__":
    cli()
