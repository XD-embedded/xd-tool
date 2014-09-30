import sys
import os
import re

import xd.tool.imp
from xd.tool.shell import call

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


__all__ = [ 'Manifest', 'NotInManifest', 'InvalidManifest' ]


class NotInManifest(Exception):
    pass

class InvalidManifest(Exception):
    pass


class Manifest(object):
    """A Manifest represents an XD-embedded manifest."""

    META_DIR_PATTERN = re.compile('^meta/(\w+)$')
    LIB_DIR_PATTERN = re.compile('^lib/(\w+)$')
    META_PKG_PATTERN = re.compile('^xd\.meta\.(\w+)$')

    @classmethod
    def meta_dir_layer(cls, dir_path):
        match = cls.META_DIR_PATTERN.match(dir_path)
        if match:
            return match.group(1)
        else:
            return None

    @classmethod
    def lib_dir_layer(cls, dir_path):
        match = cls.LIB_DIR_PATTERN.match(dir_path)
        if match:
            return match.group(1)
        else:
            return None

    @classmethod
    def meta_pkg_layer(cls, pkg_path):
        match = cls.META_PKG_PATTERN.match(pkg_path)
        if match:
            return match.group(1)
        else:
            return None

    def __init__(self, dir=None, env=os.environ, init=False):
        if not dir:
            dir = env.get('PWD') or os.getcwd()
        self.topdir = self.locate_topdir(dir)
        if not self.topdir:
            raise NotInManifest()
        self.load_config()
        self.submodules = []
        self.meta_layers = ['.']
        self.lib_layers = []
        status = call('git submodule status', path=self.topdir, quiet=True)
        for line in status.rstrip('\n').split('\n'):
            if not line:
                continue
            sha1, path, describe = line.split(maxsplit=2)
            # FIXME: add proper layer ordering, controllable via some in-layer
            # priorties or something like that.
            self.submodules.append(path)
            if self.meta_dir_layer(path):
                self.meta_layers.append(path)
            elif self.lib_dir_layer(path):
                self.lib_layers.append(path)
                log.warning('layer ordering not implemented yet!')
        if 'XD_META_PATH' in env:
            self.meta_layers = env['XD_META_PATH'].split(':')
        elif 'META_PATH' in self.config:
            self.meta_layers = self.config['META_PATH'].split(':')
        if 'XD_LIB_PATH' in env:
            self.lib_layers = env['XD_LIB_PATH'].split(':')
        elif 'LIB_PATH' in env:
            self.lib_layers = self.config['LIB_PATH'].split(':')
        log.debug('meta_layers %s', self.meta_layers)
        log.debug('lib_layers %s', self.lib_layers)
        sys.meta_path.append(xd.tool.imp.MetaImporter(self))

    @classmethod
    def locate_topdir(cls, dir):
        if dir == '/':
            return None
        if not call('git rev-parse --is-inside-work-tree',
                    path=dir, quiet=True):
            return cls.locate_topdir(os.path.dirname(dir))
        dir = call('git rev-parse --show-toplevel',
                   path=dir, quiet=True)
        dir = dir.rstrip()
        if not os.path.exists(os.path.join(dir, '.xd')):
            return cls.locate_topdir(os.path.dirname(dir))
        return os.path.realpath(dir)

    def load_config(self):
        filename = os.path.join(self.topdir, '.xd')
        source = open(filename).read()
        code = compile(source, filename, 'exec', dont_inherit=True)
        variables = {}
        exec(code, variables)
        self.config = {k: v for k, v in variables.items()
                       if not k.startswith('_') and
                       type(v) in (str, list, dict, bool) }

    def get_meta_libdir(self, name):
        libdir = os.path.join(self.topdir, 'meta', name, 'lib')
        if not os.path.isdir(libdir):
            return None
        return libdir

    def import_commands(self):
        for path in self.meta_layers:
            if not os.path.isdir(os.path.join(path, 'lib', 'cmd')):
                log.debug('no commands in %s layer', path)
                continue
            log.debug('maybe commands in %s layer', path)
            for command in xd.tool.imp.import_commands(
                    self.meta_dir_layer(path)):
                yield command
