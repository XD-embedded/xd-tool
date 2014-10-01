import os

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from xd.tool.shell import call

def add_arguments(parser):
    return

# FIXME: add usage/description help text to subparser

def run(args, manifest, env):
    if not os.path.exists('.git'):
        if not call('git init'):
            return 'git init failed'
    if not os.path.exists('.xd'):
        with open('.xd', 'w') as f:
            f.write('ABI=0\n')
        if not call('git add .xd'):
            return 'git add failed'
        if not call('git commit -m "Initial commit" -- .xd'):
            return 'git commit failed'
    if call('git rev-parse --git-dir', quiet=True) != '.git\n':
        return 'Invalid manifest git dir'
    return
