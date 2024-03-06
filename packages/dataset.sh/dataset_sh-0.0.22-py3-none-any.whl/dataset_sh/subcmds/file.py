import json

import click

from dataset_sh import open_dataset_file
from dataset_sh.typing.codegen import CodeGenerator


@click.group(name='file')
def file_cli():
    """to interact with standalone dataset.sh file"""
    pass


@file_cli.command(name='list-collections')
@click.argument('filepath', type=click.Path())
def list_collections(filepath):
    """list collections of a dataset file"""
    with open_dataset_file(filepath) as reader:
        collections = reader.collections()
        click.echo(f'Total collections: {len(collections)}')
        for coll in collections:
            click.echo(coll)


@file_cli.command(name='print-code')
@click.argument('filepath', type=click.Path())
@click.argument('collection_name')
def print_code(filepath, collection_name):
    """print usage code of the given collection on the dataset file"""
    with open_dataset_file(filepath) as reader:
        coll = reader.collection(collection_name)
        code = coll.code_usage()
        schema = coll.config.data_schema
        loader_code = CodeGenerator.generate_file_loader_code(filepath, collection_name, schema.entry_point)
        click.echo(code)
        click.echo('\n\n')
        click.echo(loader_code)


@file_cli.command(name='print-sample')
@click.argument('filepath', type=click.Path())
@click.argument('collection_name')
def print_sample(filepath, collection_name):
    """print data samples of the given collection on a dataset file"""
    with open_dataset_file(filepath) as reader:
        sample = reader.collection(collection_name).top()
        click.echo(json.dumps(sample, indent=2))
