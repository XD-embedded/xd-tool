from xd.tool.main import main
import xd.tool.log

from nose.tools import raises, with_setup
import unittest
import os
import tempfile
import shutil
from redirect import stdchannel_redirected


class tests(unittest.case.TestCase):

    def setUp(self):
        self.oldcwd = os.getcwd()
        self.oldpwd = os.environ['PWD'] or None
        self.testdir = tempfile.mkdtemp(prefix='nose-')
        os.chdir(self.testdir)
        os.environ['PWD']=self.testdir

    def tearDown(self):
        os.chdir(self.oldcwd)
        if self.oldpwd:
            os.environ['PWD'] = self.oldpwd
        shutil.rmtree(self.testdir)
        xd.tool.log.deinit()

    def test_init(self):
        with stdchannel_redirected(1):
            self.assertEqual(main(['xd', 'init']), None)
        self.assertTrue(os.path.isdir('.git'))
        self.assertTrue(os.path.isfile('.xd'))

    def test_init_twice(self):
        with stdchannel_redirected(1):
            self.assertEqual(main(['xd', 'init']), None)
        self.assertTrue(os.path.isdir('.git'))
        self.assertTrue(os.path.isfile('.xd'))
        with stdchannel_redirected(2):
            self.assertEqual(main(['xd', '-d', 'init']), None)
        self.assertTrue(os.path.isdir('.git'))
        self.assertTrue(os.path.isfile('.xd'))

    def test_init_fail(self):
        with open('.git', 'w') as f:
            f.write('foobar')
        self.assertNotEqual(main(['xd', 'init']), None)
