import os
import sh
sh.Command._call_args['err_to_out'] = True
from sh import git
from xd.tool.shell import call
from xd.tool.os import pushd

import logging
log = logging.getLogger(__name__)


def run_status(args, manifest, env, subparser):
    layers = manifest.meta_layers + manifest.lib_layers
    layer_name_max_length = max(map(len, layers))
    for layer in manifest.meta_layers:
        if layer == '.':
            continue
        with pushd(layer):
            url = git.config('remote.origin.url')
        print("%%-%ds  %%s"%(layer_name_max_length)%(layer, url.strip()))
    return


layers = {
    'meta/core' : 'https://github.com/XD-embedded/xd-meta-core.git',
}


def run_list(args, manifest, env, subparser):
    layer_name_max_length = max(map(len, layers.keys()))
    for name, url in layers.items():
        print("%%-%ds  %%s"%(layer_name_max_length)%(name, url))


def run_add(args, manifest, env, subparser):
    try:
        url = layers[args.layer]
    except KeyError:
        log.error("Unknown layer: %s", args.layer)
        log.info("Use 'xd layer list' to show available layers")
        return "unknown layer"
    if not call('git submodule add %s %s'%(url, args.layer)):
        return 'git submodule add failed'
    if not call('git commit -m "Add %s layer" -- %s .gitmodules'%(
            args.layer, args.layer)):
        return 'git commit failed'


subcommands = {}

parser_help = 'Manage manifest layers'

def add_arguments(parser):
    globals()['parser'] = parser
    subparsers = parser.add_subparsers(
        title='layer commands', dest='subcommand')
    subparser = subparsers.add_parser(
        'status', help='Show the layer status of the manifest')
    subcommands['status'] = (run_status, subparser)
    subparser = subparsers.add_parser(
        'add', help='Add a layer to the manifest')
    subcommands['add'] = (run_add, subparser)
    subparser.add_argument(
        'layer', help='Layer to add')
    subparser = subparsers.add_parser(
        'list', help='List known layers, which can be added to manifest')
    subcommands['list'] = (run_list, subparser)
    return


def run(args, manifest, env):
    if not args.subcommand:
        parser.print_usage()
        return
    if not manifest:
        log.error("Manifest not found")
        return 1
    cmd, subparser = subcommands[args.subcommand]
    return cmd(args, manifest, env, subparser)
