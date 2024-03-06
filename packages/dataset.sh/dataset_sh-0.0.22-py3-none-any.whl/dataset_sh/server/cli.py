#!/usr/bin/env python3
import os.path
from dataclasses import dataclass
from getpass import getpass
from urllib.parse import urlparse

import click

from dataset_sh.server.core import RepoServerConfig


@dataclass
class RepoServerConfigCtx:
    path: str
    config: RepoServerConfig
    is_new: bool = False


@click.group(name='dataset-sh-server-config')
@click.option(
    '--config', '-c',
    envvar='DATASET_SH_SERVER_CONFIG_FILE',
    help='location of server config file.',
    default='./dataset-sh-server-config.json',
    type=click.Path()
)
@click.pass_context
def cli(ctx, config):
    """config dataset.sh server"""
    if os.path.exists(config):
        ctx.obj = RepoServerConfigCtx(path=config, config=RepoServerConfig.load_from_file(config))
    else:
        ctx.obj = RepoServerConfigCtx(path=config, config=RepoServerConfig(), is_new=True)


@click.command(name='set-password')
@click.argument('username')
@click.pass_obj
def set_password(ctx, username):
    """set password for user, and generate a new access key"""
    password = getpass('Password:')
    ctx.config.update_password(username, password)
    ctx.config.write_to_file(ctx.path)
    key = ctx.config.generate_key(username, password)
    click.echo(f'Access Key: {key}\n')
    click.echo(f'Add this key to your client with this command: ')
    click.echo(f'  dataset.sh profile add -h {ctx.config.hostname}')


@click.command(name='init')
@click.pass_obj
def init_config(ctx):
    """Create an empty config file"""
    ctx.config.write_to_file(ctx.path)


@click.command(name='set-hostname')
@click.argument('hostname')
@click.pass_obj
def set_hostname(ctx, hostname):
    """set server hostname"""
    if not is_valid_url(hostname):
        click.echo(f'invalid hostname {hostname}')
        raise click.Abort()
    ctx.config.hostname = hostname
    ctx.config.write_to_file(ctx.path)


def is_valid_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ['http', 'https']


cli.add_command(set_password)
cli.add_command(init_config)
cli.add_command(set_hostname)

if __name__ == '__main__':  # pragma: no cover
    cli()
