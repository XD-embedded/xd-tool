import sys
import os
import re
import sh
from sh import git

import xd.tool.imp
from xd.tool.os import *

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

    LIB_DIR_PATTERN = re.compile('^lib/(\w+)$')
    LAYER_PKG_PATTERN = re.compile('^xd\.(\w+(\.\w+)*)')

    @classmethod
    def lib_dir_layer(cls, dir_path):
        match = cls.LIB_DIR_PATTERN.match(dir_path)
        if match:
            return match.group(1)
        else:
            return None

    @classmethod
    def layer_package_to_dir(cls, pkg_path):
        match = cls.LAYER_PKG_PATTERN.match(pkg_path)
        if match:
            return match.group(1)
        else:
            return None

    @classmethod
    def layer_dir_to_package(cls, dir_path):
        return 'xd.%s'%(dir_path.replace(os.sep, '.'))

    def __init__(self, dir=None, env=os.environ, init=False):
        if not dir:
            dir = env.get('PWD') or os.getcwd()
        self.topdir = self.locate_topdir(dir)
        if not self.topdir:
            raise NotInManifest()
        self.load_config()
        self.submodules = []
        self.xd_layers = ['.']
        self.lib_layers = []
        with pushd(self.topdir):
            status = git.submodule.status()
        for line in status.rstrip('\n').split('\n'):
            if not line:
                continue
            sha1, path, describe = line.split(maxsplit=2)
            # FIXME: add proper layer ordering, controllable via some in-layer
            # priorties or something like that.
            self.submodules.append(path)
            if self.lib_dir_layer(path):
                self.lib_layers.append(path)
            else:
                self.xd_layers.append(path)
        if 'XD_LAYER_PATH' in env:
            self.xd_layers = env['XD_LAYER_PATH'].split(':')
        elif 'LAYER_PATH' in self.config:
            self.xd_layers = self.config['LAYER_PATH'].split(':')
        if 'XD_LIB_PATH' in env:
            self.lib_layers = env['XD_LIB_PATH'].split(':')
        elif 'LIB_PATH' in env:
            self.lib_layers = self.config['LIB_PATH'].split(':')
        log.debug('xd_layers %s', self.xd_layers)
        log.debug('lib_layers %s', self.lib_layers)
        sys.meta_path.append(xd.tool.imp.LayerImporter(self))

    @classmethod
    def locate_topdir(cls, path):
        if path == '/':
            return None
        with pushd(path):
            try:
                git('rev-parse', '--is-inside-work-tree')
            except sh.ErrorReturnCode:
                return cls.locate_topdir(os.path.dirname(path))
            path = git('rev-parse', '--show-toplevel')
            path = path.rstrip()
            if not os.path.exists(os.path.join(path, '.xd')):
                return cls.locate_topdir(os.path.dirname(path))
        return os.path.realpath(path)

    def load_config(self):
        filename = os.path.join(self.topdir, '.xd')
        source = open(filename).read()
        code = compile(source, filename, 'exec', dont_inherit=True)
        variables = {}
        exec(code, variables)
        self.config = {k: v for k, v in variables.items()
                       if not k.startswith('_') and
                       type(v) in (str, list, dict, bool) }

    def get_layer_libdir(self, package):
        libdir = os.path.join(self.topdir, package.replace('.', os.sep), 'lib')
        if not os.path.isdir(libdir):
            log.debug('layer libdir not found: %s'%(libdir))
            return None
        return libdir

    def import_commands(self):
        for path in self.xd_layers:
            if not os.path.isdir(os.path.join(path, 'lib', 'cmd')):
                log.debug('no commands in %s layer', path)
                continue
            log.debug('maybe commands in %s layer', path)
            for command in xd.tool.imp.import_commands(path):
                yield command
