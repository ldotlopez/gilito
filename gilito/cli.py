from pathlib import Path

import click

import gilito
from gilito import LogBook


#
# Define options
#

opt_source = click.option("-s", "--source", multiple=True, required=True)

opt_loader = click.option(
    "--loader",
    required=True,
    help="Loader to use",
    type=str,
)

opt_mapper = click.option(
    "--mapper",
    required=False,
    help="Rules to apply to use",
    type=str,
)

opt_processors = click.option(
    "--processor",
    multiple=True,
    required=False,
    help="Rules to apply to use",
    type=str,
    default=[],
)

opt_dumper = click.option(
    "--dumper", required=False, help="Dumper to use", type=str, default="csv"
)


def _expand_paths(*paths: Path):
    for p in paths:
        if p.is_dir():
            children = list(p.iterdir())
            yield from _expand_paths(*children)

        elif p.is_file():
            yield from [p]

        else:
            pass


@click.command()
@opt_source
@opt_loader
@opt_mapper
@opt_processors
@opt_dumper
def cli(source, loader, mapper, processor, dumper):
    def _it(it):
        yield from it

    sources = sorted((Path(x) for x in source))
    sources = (
        x for x in _expand_paths(*sources) if x.is_file() and not x.name.startswith(".")
    )

    # Load data into memory
    sources_data = _it((x.read_bytes() for x in sources))

    # Parse raw data
    ldr = gilito.get_plugin(loader)()
    sources_data = _it((ldr.load(x) for x in sources_data))

    # Map data into Logbooks and Transactions
    mpr = gilito.get_plugin(mapper)()
    logbooks = _it((mpr.map(x) for x in sources_data))

    # Merge all logbooks
    log = LogBook()
    log.merge(*logbooks)

    # Process logbook
    for proc in processor:
        plg = gilito.get_plugin(proc)()
        plg.process(log)

    # Dump
    plg = gilito.get_plugin(dumper)()
    print(plg.dump(log).decode("utf-8"))
