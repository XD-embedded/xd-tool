from xd.tool.main import main

from nose.tools import raises, with_setup

import logging


def test_init_no_args():
    main(['xd'])

def test_init_early_args():
    main(['xd', '-d'])

