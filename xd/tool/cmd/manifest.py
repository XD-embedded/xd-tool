import os

import logging
log = logging.getLogger(__name__)

def add_arguments(parser):
    return

# FIXME: add usage/description help text to subparser

def run(args, manifest, env):
    if not manifest:
        log.error("Manifest not found")
        return 1
    print('Metadata layers:')
    if manifest.meta_layers:
        print('  %s'%('\n  '.join(manifest.meta_layers)))
    if manifest.lib_layers:
        print('Library layers:\n  %s'%('\n  '.join(manifest.lib_layers)))
    return
