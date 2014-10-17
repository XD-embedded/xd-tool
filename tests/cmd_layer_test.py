from xd.tool.main import main

from case import *
from redirect import *
import sys
import os
import stat
import shutil
import configparser
import sh
import importlib


class tests(TestCase):

    def setUp(self):
        super(tests, self).setUp()

    def test_layer_nosubcmd(self):
        main(['xd', 'layer'])
        self.assertRegex(sys.stdout.getvalue(), 'usage: ')

    def test_layer_list(self):
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', 'init']))
            self.assertIsNone(main(['xd', 'layer', 'list']))

    def test_layer_list_no_manifest(self):
        with self.assertLogs('xd.tool.cmd.layer', level='ERROR') as logs:
            with stdchannels_redirected():
                self.assertEqual(main(['xd', 'layer', 'list']), 1)
        self.assertEqual(logs.records[0].message, 'Manifest not found')

    def test_layer_add(self):
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', 'init']))
            self.assertIsNone(main(['xd', 'layer', 'add', 'build/core']))

    def test_layer_add_none(self):
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', 'init']))
            with self.assertRaises(SystemExit):
                main(['xd', 'layer', 'add'])

    def test_layer_add_unknown(self):
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', 'init']))
            self.assertIsNotNone(main(['xd', 'layer', 'add', 'FOOBAR']))

    def test_layer_add_fail_1(self):
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', 'init']))
        os.chmod('.', stat.S_IREAD|stat.S_IEXEC)
        with stdchannels_redirected():
            self.assertIsNotNone(main(['xd', 'layer', 'add', 'build/core']))

    def test_layer_add_fail_2(self):
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', 'init']))
        os.chmod('.git/refs/heads', stat.S_IREAD)
        with stdchannels_redirected():
            self.assertIsNotNone(main(['xd', 'layer', 'add', 'build/core']))

    def test_layer_status_empty(self):
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', 'init']))
            self.assertIsNone(main(['xd', 'layer', 'status']))

    def test_layer_status_nonempty(self):
        with stdchannels_redirected():
            self.assertIsNone(main(['xd', 'init']))
            self.assertIsNone(main(['xd', 'layer', 'add', 'build/core']))
            self.assertIsNone(main(['xd', 'layer', 'status']))
        stdout_lines = sys.stdout.getvalue().splitlines()
        self.assertRegex(stdout_lines[-1], 'build/core .*')
