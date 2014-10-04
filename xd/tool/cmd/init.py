import os
import sh
sh.Command._call_args['err_to_out'] = True
from sh import git
from xd.tool.shell import call

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

parser_help = 'Initialize manifest'

def add_arguments(parser):
    return

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
    try:
        git_dir = git('rev-parse', git_dir=True)
    except sh.ErrorReturnCode as e:
        git_dir = None
    if git_dir != '.git\n':
        return 'invalid manifest git dir'
    return
