from xd.tool.main import main
import xd.tool.log

from nose.tools import raises, with_setup
import unittest
import sys
import os
import stat
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
        shutil.rmtree(self.testdir, ignore_errors=True)
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

    def test_init_fail_1(self):
        with open('.git', 'w') as f:
            f.write('foobar')
        with stdchannel_redirected(2):
            self.assertNotEqual(main(['xd', 'init']), None)

    def test_init_fail_2(self):
        with open('.git', 'w') as f:
            f.write('foobar')
        with open('.xd', 'w') as f:
            f.write('foobar')
        self.assertNotEqual(main(['xd', 'init']), None)

    def test_init_fail_3(self):
        os.chmod('.', stat.S_IREAD|stat.S_IEXEC)
        with stdchannel_redirected(2):
            self.assertNotEqual(main(['xd', 'init']), None)

    def test_init_fail_4(self):
        xd.tool.shell.call('git init', quiet=True)
        os.chmod('.git/refs/heads', stat.S_IREAD)
        with stdchannel_redirected(2):
            self.assertNotEqual(main(['xd', 'init']), None)
