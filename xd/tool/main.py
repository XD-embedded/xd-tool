import logging
import warnings
import argparse
import sys
import os

import xd.tool
import xd.tool.log


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
    else:
        log.setLevel(logging.INFO)

    log.debug('XD-tool %s', xd.tool.__version__)

    # Establish the manifest stack order
    from xd.tool.manifest import Manifest, NotInManifest
    try:
        manifest = Manifest()
        log.debug('manifest %s', manifest.topdir)
        os.chdir(manifest.topdir)
        manifest.extend_path(sys.path)
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

    # Add builtin subcommands
    from xd.tool.commands import add_commands
    add_commands(subparsers, 'xd.tool.cmd')
    # Add manifest subcommands
    if manifest:
        manifest.add_commands(subparsers)

    args = parser.parse_args(remaining_args)
    log.debug('args: %r', args)

    if not args.command:
        parser.print_usage()
        return

    return args.run(args, manifest, os.environ)
