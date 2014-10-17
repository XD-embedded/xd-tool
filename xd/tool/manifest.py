import sys
import os
import re
import sh
from sh import git
import configparser
import importlib
import pkgutil

import xd
from xd.tool.commands import *
from xd.tool.os import *
from xd.tool.layer import *

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


__all__ = ['Manifest', 'NotInManifest', 'InvalidManifest']


class NotInManifest(Exception):
    pass

class InvalidManifest(Exception):
    pass


class Manifest(object):
    """A Manifest represents an XD-embedded manifest."""

    def __init__(self, dir_=None, env=None):
        if dir_ is None:
            dir_ = (env or os.environ).get('PWD') or os.getcwd()
        self.topdir = self.locate_topdir(dir_)
        if not self.topdir:
            raise NotInManifest()
        self.layers = []
        self.configfile = os.path.join(self.topdir, '.xd')
        self.config = configparser.ConfigParser()
        self.config.read(self.configfile)
        with pushd(self.topdir):
            status = git.submodule.status()
        for line in status.rstrip('\n').split('\n'):
            if not line:
                continue
            sha1, path, describe = line.split(maxsplit=2)
            try:
                layer = Layer(self, path, commit=sha1)
            except NotALayer:
                log.debug('Ignoring non-layer submodule %s', path)
                continue
            self.layers.append(layer)
        with pushd(self.topdir):
            try:
                sha1 = git('rev-parse', 'HEAD', '--')
            except sh.ErrorReturnCode as e:
                log.debug('git rev-parse HEAD on manifest failed\n%s', e)
                sha1 = None
        try:
            layer = Layer(self, '.', commit=sha1)
            self.layers.append(layer)
        except NotALayer:
            log.debug('Manifest is not a layer')
        self.layers.sort(key=lambda l: l.priority())

    def extend_path(self, path):
        for layer in self.layers:
            path.insert(0, layer.path)
        xd.__path__ = pkgutil.extend_path(xd.__path__, xd.__name__)

    def get_priority(self, layer_name):
        try:
            return self.config['priority'].getint(layer_name)
        except KeyError:
            return None

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
            configfile = os.path.join(path, '.xd')
            if not os.path.exists(configfile):
                return cls.locate_topdir(os.path.dirname(path))
            config = configparser.ConfigParser()
            config.read(configfile)
            if not config.has_section('manifest'):
                return cls.locate_topdir(os.path.dirname(path))
        return os.path.realpath(path)

    def add_commands(self, subparsers):
        for layer in self.layers:
            commands_package = layer.config.get('commands')
            if not commands_package:
                continue
            log.debug('commands in %s layer', layer.submodule)
            add_commands(subparsers, commands_package)
