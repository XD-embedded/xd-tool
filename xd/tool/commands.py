import sys
import os
import re
import importlib.util
import pkgutil

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


__all__ = ['add_commands']


def add_commands(subparsers, path):
    """Add XD-embedded commands from a given package to ArgumentParser.

    Arguments:
    subparsers -- ArgumentParser subparser object
    package -- Python package path
    """
    log.debug('importing %s', path)
    try:
        del sys.modules[path]
    except KeyError:
        pass
    try:
        package = importlib.import_module(path)
    except Exception as e:
        log.warning('failed to import commands package %s',
                    path, exc_info=True)
        return
    log.debug('commands package: %s', path)
    for (finder, name, ispkg) in pkgutil.iter_modules(package.__path__):
        if ispkg:
            continue
        try:
            command = importlib.import_module('.' + name, path)
        except Exception as e:
            log.warning('failed to import %s command: %s',
                        path, name, exc_info=True)
            continue
        if not getattr(command, 'run', None):
            log.warning('skipping command module without run function: %s',
                        name)
            continue
        log.debug('command: %s'%(name))
        name = command.__name__.split('.')[-1]
        parser_help = getattr(command, 'parser_help', None)
        if parser_help is None:
            log.warning('command %s missing help text'%(command.__name__))
        parser = subparsers.add_parser(name, help=parser_help)
        command.add_arguments(parser)
        parser.set_defaults(run=command.run)
