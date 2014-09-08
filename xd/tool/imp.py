import os
import re
import importlib.util
import pkgutil

import logging
log = logging.getLogger(__name__)


class MetaImporter(object):
    """A meta path finder for XD-embedded metadata library packages.

    Instances of this class can be used to load XD-embedded metadata library
    packages into the xd.meta namespace.

    To use it, add an instance of it to sys.meta_path.
    """

    def __init__(self, manifest):
        """Constructor.

        Arguments:
        manifest -- XD-embedded manifest containing the metadata layers to use
        """
        self.manifest = manifest

    def find_spec(self, fullname, path, target=None):
        """The hook method called by the Python import system.

        When searching for a module, if the module is not found in
        sys.modules, Python will call this method on objects in sys.meta_path.

        Arguments:
        fullname -- the Python module name, fx. "xd.meta.core"
        path -- import path (ignored)
        target -- target module (ignored)
        """
        log.debug('find_spec(%s, %s, %s)', fullname, path, target)
        if fullname.startswith('.'):
            return None
        meta_name = self.manifest.meta_pkg_layer(fullname)
        if meta_name:
            log.debug('looking for layer %s', meta_name)
            libdir = self.manifest.get_meta_libdir(meta_name)
            spec = importlib.util.spec_from_file_location(
                fullname, os.path.join(libdir, '__init__.py'))
            return spec


def import_commands(layer=None):
    """Import all XD-embedded commands from a given layer (or XD-tool itself).

    Arguments:
    layer -- Name of layer (or None for XD-tool commands)

    This function is a generator, yielding the commands available, in the form
    of the Python module containing the command.
    """
    log.debug('layer=%s', layer)
    if layer is None:
        package = 'xd.tool.cmd'
    else:
        package = 'xd.meta.%s.cmd'%(layer)
    try:
        commands = importlib.import_module(package)
    except ImportError:
        return
    log.debug('commands: %s', commands)
    for (finder, name, ispkg) in pkgutil.iter_modules(
            commands.__path__):
        if ispkg:
            continue
        try:
            command = importlib.import_module('.' + name, package)
        except Exception as e:
            log.warning('failed to import %s c ommand: %s', layer, name,
                        exc_info=True)
            continue
        if not getattr(command, 'run'):
            log.debug('skipping command module without run function: %s', name)
            continue
        log.debug('command: %s'%(name))
        yield command
