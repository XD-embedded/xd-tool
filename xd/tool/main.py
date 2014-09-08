import logging
import argparse
import sys
import os

import xd.tool
import xd.tool.log
import xd.tool.cmd
from xd.tool.manifest import *


def main(argv=sys.argv):
    """The main() function of XD-tool."""
    prog = os.path.basename(argv[0])
    version = xd.tool.__version__

    # Create parser to catch bakery '-d/--debug' early enough to be useful
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Debug the XD-tool command')
    parser.add_argument('command', nargs='?')
    parser.add_argument('command_args', nargs=argparse.REMAINDER)
    early_args, remaining_args = parser.parse_known_args(argv[1:])
    if early_args.command:
        remaining_args += [early_args.command] + early_args.command_args

    # Initialize logger
    xd.tool.log.init()
    log = logging.getLogger(__package__)
    if early_args.debug:
        log.setLevel(logging.DEBUG)

    log.debug('XD-tool %s', xd.tool.__version__)

    # Establish the manifest stack order
    try:
        manifest = Manifest()
        log.debug('manifest=%s', manifest.topdir)
        xd.tool.shell.chdir(manifest.topdir, quiet=True)
    except NotInManifest:
        manifest = None
        log.debug('no manifest')

    # Initialize the complete argument parser
    parser = argparse.ArgumentParser(
        description='''XD-tool -- the command-line tool for XD-embedded.
        XD-tool comes with a few basic manifest maintenance commands.
        Additional commands must be provided by the metadata layers.''')
    parser.add_argument('--version', action='version',
                        version='XD-tool %(version)s'%locals())
    parser.add_argument(
        '-d', '--debug', dest='bakery_debug',
        action='store_true', default=early_args.debug,
        help='Debug the XD-tool')
    subparsers = parser.add_subparsers(title='XD commands', dest='command')

    commands = {}
    def add_parser(command):
        name = command.__name__.split('.')[-1]
        parser = subparsers.add_parser(name)
        command.add_arguments(parser)
        commands[name] = command
    # Add builtin subcommands
    for command in xd.tool.imp.import_commands():
        add_parser(command)
    # Add manifest subcommands
    if manifest:
        #manifest.add_commands(subparsers)
        for command in manifest.import_commands():
            add_parser(command)

    args = parser.parse_args(remaining_args)
    log.debug('args: %r', args)

    if not args.command:
        parser.print_usage()
        return

    command = commands[args.command]
    return command.run(args, manifest, os.environ)
