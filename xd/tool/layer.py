import os
import configparser

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


__all__ = [ 'Layer', 'NotALayer' ]


class NotALayer(Exception):
    pass


class Layer(object):
    """A Layer represents a layer of an XD-embedded manifest"""

    def __init__(self, manifest, submodule, commit=None):
        self.manifest = manifest
        self.submodule = submodule
        if submodule == '.':
            self.path = manifest.topdir
        else:
            self.path = os.path.join(manifest.topdir, submodule)
        self.commit = commit
        self.configfile = os.path.join(self.path, '.xd')
        config = configparser.ConfigParser()
        if os.path.exists(self.configfile):
            config.read(self.configfile)
        if not config.has_section('layer'):
            raise NotALayer()
        self.config = config['layer']

    def priority(self):
        priority = self.manifest.get_priority(self.submodule)
        if priority is None and self.config:
            priority = self.config.getint('priority', fallback=None)
        if priority is None:
            log.warning('No priority for layer %s', self.submodule)
            return None
        return priority
