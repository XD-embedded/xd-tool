from xd.tool.main import main
import xd.tool.log

import unittest
from unittest.mock import patch
from nose.tools import raises, with_setup
import sys
import os
import stat
import tempfile
import shutil
from redirect import *


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

    def test_layer_nosubcmd(self):
        main(['xd', 'layer'])
        self.assertRegex(sys.stdout.getvalue(), 'usage: ')

    def test_layer_list(self):
        with stdchannels_redirected():
            self.assertEqual(main(['xd', 'init']), None)
            self.assertEqual(main(['xd', 'layer', 'list']), None)

    def test_layer_list_no_manifest(self):
        with self.assertLogs('xd.tool.cmd.layer', level='ERROR') as logs:
            with stdchannels_redirected():
                self.assertEqual(main(['xd', 'layer', 'list']), 1)
        self.assertEqual(logs.records[0].message, 'Manifest not found')

    def test_layer_add(self):
        with stdchannels_redirected():
            self.assertEqual(main(['xd', 'init']), None)
            self.assertEqual(main(['xd', 'layer', 'add', 'build/core']), None)

    def test_layer_add_none(self):
        with stdchannels_redirected():
            self.assertEqual(main(['xd', 'init']), None)
            with self.assertRaises(SystemExit):
                main(['xd', 'layer', 'add'])

    def test_layer_add_unknown(self):
        with stdchannels_redirected():
            self.assertEqual(main(['xd', 'init']), None)
            self.assertNotEqual(main(['xd', 'layer', 'add', 'FOOBAR']), None)

    def test_layer_add_fail_1(self):
        with stdchannels_redirected():
            self.assertEqual(main(['xd', 'init']), None)
        os.chmod('.', stat.S_IREAD|stat.S_IEXEC)
        with stdchannels_redirected():
            self.assertNotEqual(main(['xd', 'layer', 'add', 'build/core']), None)

    def test_layer_add_fail_2(self):
        with stdchannels_redirected():
            self.assertEqual(main(['xd', 'init']), None)
        os.chmod('.git/refs/heads', stat.S_IREAD)
        with stdchannels_redirected():
            self.assertNotEqual(main(['xd', 'layer', 'add', 'build/core']), None)

    def test_layer_status_empty(self):
        with stdchannels_redirected():
            self.assertEqual(main(['xd', 'init']), None)
            self.assertEqual(main(['xd', 'layer', 'status']), None)

    def test_layer_status_nonempty(self):
        with stdchannels_redirected():
            self.assertEqual(main(['xd', 'init']), None)
            self.assertEqual(main(['xd', 'layer', 'add', 'build/core']), None)
            self.assertEqual(main(['xd', 'layer', 'status']), None)
        stdout_lines = sys.stdout.getvalue().splitlines()
        self.assertRegex(stdout_lines[-1], 'build/core .*')
