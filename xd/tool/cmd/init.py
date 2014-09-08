import os

import logging
log = logging.getLogger(__name__)

from xd.tool.shell import call

def add_arguments(parser):
    return

# FIXME: add usage/description help text to subparser

def run(args, manifest, env):
    if not os.path.exists('.xd'):
        with open('.xd', 'w') as f:
            f.write('ABI=0\n')
        log.info('Wrote .xd file')
    if call('git rev-parse --git-dir', quiet=True) is None:
        if not call('git init'):
            return 'git init failed'
    return
