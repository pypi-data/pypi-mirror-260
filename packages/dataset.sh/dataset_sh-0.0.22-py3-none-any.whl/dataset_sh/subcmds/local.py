import json

import click

from dataset_sh.clients.obj import LocalStorage
from dataset_sh.utils.misc import parse_tags


def _get_dataset_version(name, version, tag):
    dataset = LocalStorage().dataset(name)
    if version:
        dv = dataset.version(version)
    elif tag:
        dv = dataset.tag(tag)
    else:
        dv = dataset.latest()
    return dv


@click.group(name='local')
def local_cli():
    """to interact with dataset.sh local storage"""
    pass


@local_cli.command(name='import-as-latest')
@click.argument('name')
@click.argument('file')
@click.option('--tag', '-t', default='')
def import_(name, file, tag):
    """import dataset from file, and automatically tag it as latest"""
    click.echo(f'importing local file from {file}')
    LocalStorage().dataset(name).import_file(file_path=file, tags=parse_tags(tag))


@local_cli.command(name='import')
@click.argument('name')
@click.argument('file')
@click.option('--tag', '-t', default='latest')
def import_(name, file, tag):
    """import dataset from file and do not tag it as latest"""
    click.echo(f'importing local file from {file}')
    LocalStorage().dataset(name).import_file(file_path=file, tags=parse_tags(tag), as_latest=False)


@local_cli.command(name='meta')
@click.argument('name')
@click.option('--version', '-v', help='use this option to select version', default=None)
@click.option('--tag', '-t', help='use this option to select version with tag', default='latest')
def print_meta(name, version, tag):
    """print metadata of a dataset"""
    dv = _get_dataset_version(name, version, tag)
    if dv.exists():
        meta = dv.meta()
        if meta:
            click.echo(json.dumps(meta, indent=2))
    else:
        raise ValueError(f'{dv} do not exists.')


@local_cli.command(name='list-collections')
@click.argument('name')
@click.option('--version', '-v', help='use this option to select version', default=None)
@click.option('--tag', '-t', help='use this option to select version with tag', default='latest')
def list_collections(name, version, tag):
    """
    list collections of a dataset
    """
    dv = _get_dataset_version(name, version, tag)
    if dv.exists():
        meta = dv.meta_object()
        click.echo(f'Total collections: {len(meta.collections)}')
        for coll in meta.collections:
            click.echo(coll.name)
    else:
        raise ValueError(f'{dv} do not exists.')


@local_cli.command(name='print-code')
@click.argument('name')
@click.argument('collection_name')
@click.option('--version', '-v', help='use this option to select version', default=None)
@click.option('--tag', '-t', help='use this option to select version with tag', default='latest')
def print_code(name, collection_name, version, tag):
    dv = _get_dataset_version(name, version, tag)
    if dv.exists():
        code = dv.usage_code(collection_name)
        click.echo(code)
    else:
        raise ValueError(f'{dv} do not exists.')


@local_cli.command(name='print-sample')
@click.argument('name')
@click.argument('collection_name')
@click.option('--version', '-v', help='use this option to select version', default=None)
@click.option('--tag', '-t', help='use this option to select version with tag', default='latest')
def print_sample(name, collection_name, version, tag):
    dv = _get_dataset_version(name, version, tag)
    if dv.exists():
        samples = dv.sample(collection_name)
        click.echo(json.dumps(samples, indent=2))

    else:
        raise ValueError(f'{dv} do not exists.')


@local_cli.command(name='remove')
@click.argument('name')
@click.option('--force', '-f', default=False, help='Force remove dataset without confirmation.', is_flag=True)
def remove(name, force):
    """remove a managed dataset"""
    dataset = LocalStorage().dataset(name)
    do_remove = False
    if force:
        do_remove = True
    else:
        confirmation = click.prompt(f'Are you sure you want to remove all versions of dataset {name}? (y/N): ')
        if confirmation.lower() == 'y':
            do_remove = True

    if do_remove:
        dataset.delete()


@local_cli.command(name='remove-version')
@click.argument('name')
@click.option('--version', '-v', help='use this option to select version', default=None)
@click.option('--tag', '-t', help='use this option to select version with tag', default=None)
@click.option('--force', '-f', default=False, help='Force remove dataset without confirmation.', is_flag=True)
def remove_version(name, version, tag, force):
    """remove a managed dataset"""
    dv = _get_dataset_version(name, version, tag)
    do_remove = False
    if force:
        do_remove = True
    else:
        confirmation = click.prompt(f'Are you sure you want to remove all versions of dataset {name}? (y/N): ')
        if confirmation.lower() == 'y':
            do_remove = True

    if do_remove:
        dv.delete()


@local_cli.command(name='list')
@click.option('--namespace', '-n', help='select dataset store space to list.', default=None)
def list_datasets(namespace):
    """list datasets"""
    if namespace:
        items = LocalStorage().namespace(namespace).datasets()
    else:
        items = LocalStorage().datasets()

    click.echo(f'\nFound {len(items)} datasets:\n')
    items = sorted(items, key=lambda x: f'{x.namespace}/{x.dataset_name}')
    for item in items:
        click.echo(f'  {item.namespace}/{item.dataset_name}')
    click.echo('')


@local_cli.command(name='list-version')
@click.argument('name')
def list_dataset_versions(name):
    """list dataset versions"""
    dataset = LocalStorage().dataset(name)
    versions = dataset.versions()

    click.echo(f'\nFound {len(versions)} versions:\n')
    for item in versions:
        click.echo(f'  {item.version}')
    click.echo('')


@local_cli.command(name='tag')
@click.argument('name')
@click.argument('tag')
@click.argument('version')
def tag_dataset_version(name, tag, version):
    """Tag dataset version"""
    dataset = LocalStorage().dataset(name)
    dataset.set_tag(tag=tag, version=version)


@local_cli.command(name='untag')
@click.argument('name')
@click.argument('tag')
def untag_dataset_version(name, tag):
    """Remove dataset version tag"""
    dataset = LocalStorage().dataset(name)
    dataset.remove_tag(tag)


@local_cli.command(name='tag-info')
@click.argument('name')
@click.argument('tag')
def print_tag_info(name, tag):
    """Print dataset version tag information"""
    dataset = LocalStorage().dataset(name)
    tagged_version = dataset.resolve_tag(tag=tag)
    if tagged_version:
        click.echo(f"{tag} : {tagged_version}")
    else:
        click.echo(f"{tag} do not exists")
