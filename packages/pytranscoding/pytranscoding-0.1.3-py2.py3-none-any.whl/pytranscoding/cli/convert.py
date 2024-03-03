import time
import yaml

import click

from .main import *
from .config import *

from ..pytranscoding import Transcoder


@main.group(context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def convert(env):
    """subcommands for manae workspaces for pytranscoding"""
    # banner("User", env.__dict__)
    pass


@convert.command()
@click.pass_obj
@click.option("--root", default='.')
@click.option("--overwrite", default=False)
@click.option("--save_model", default=True)
def sync(env, root, overwrite, save_model):
    """Explore and Syncronize media files information"""
    # force config loading
    config.callback()

    tc = Transcoder(overwrite=overwrite, save_model=save_model)
    tc.load_model()
    tc.sync()

    # TODO: add your new workspace configuratoin folder here ...


@convert.command()
@click.pass_obj
@click.option("--retry", default=1)
@click.option("--sleep", default=60)
@click.option("--pattern", multiple=True, default=['.*'])
@click.option("--force", default=False)
@click.option("--shuffle", default=False)
@click.option("--dryrun", default=False)
def apply(
    env,
    retry,
    sleep,
    pattern,
    force,
    shuffle,
    dryrun,
    ):
    """List existing workspaces for pytranscoding"""
    # force config loading
    config.callback()

    while retry != 0:
        tc = Transcoder()
        tc.apply(
            pattern=pattern,
            force=force,
            shuffle=shuffle,
            dryrun=dryrun, 
        )
        retry -= 1
        if retry and sleep > 0:
            time.sleep(sleep)

    foo = 1
    # TODO: add your new workspace configuratoin folder here ...
