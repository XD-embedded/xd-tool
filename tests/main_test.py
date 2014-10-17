from xd.tool.main import main

from case import *
from redirect import *
import sys


class tests(TestCase):

    def test_main_no_args(self):
        main(['xd'])

    def test_main_early_args(self):
        with stdchannels_redirected():
            main(['xd', '-d'])
