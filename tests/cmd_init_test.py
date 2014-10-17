from xd.tool.main import main

from case import *
from redirect import *
import os
import stat
import sh


class tests(TestCase):

    def test_init(self):
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', 'init']))
        self.assertTrue(os.path.isdir('.git'))
        self.assertTrue(os.path.isfile('.xd'))

    def test_init_twice(self):
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', 'init']))
        self.assertTrue(os.path.isdir('.git'))
        self.assertTrue(os.path.isfile('.xd'))
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', '-d', 'init']))
        self.assertTrue(os.path.isdir('.git'))
        self.assertTrue(os.path.isfile('.xd'))

    def test_init_fail_1(self):
        with open('.git', 'w') as f:
            f.write('foobar')
        with stdchannels_redirected():
            self.assertNotEqual(main(['xd', 'init']), None)

    def test_init_fail_2(self):
        with open('.git', 'w') as f:
            f.write('foobar')
        with open('.xd', 'w') as f:
            f.write('foobar')
        self.assertNotEqual(main(['xd', 'init']), None)

    def test_init_fail_3(self):
        os.chmod('.', stat.S_IREAD|stat.S_IEXEC)
        with stdchannels_redirected():
            self.assertNotEqual(main(['xd', 'init']), None)

    def test_init_fail_4(self):
        sh.git.init()
        os.chmod('.git/refs/heads', stat.S_IREAD)
        with stdchannels_redirected():
            self.assertNotEqual(main(['xd', 'init']), None)
