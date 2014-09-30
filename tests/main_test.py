from xd.tool.main import main
from nose.tools import raises, with_setup
import logging
from redirect import stdchannel_redirected


def test_main_no_args():
    main(['xd'])


def test_main_early_args():
    with stdchannel_redirected(2):
        main(['xd', '-d'])

