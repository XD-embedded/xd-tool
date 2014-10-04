import xd.tool.shell

import unittest
from nose.tools import raises, with_setup

import os
import tempfile
import glob
import shutil

class tests(unittest.case.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        self.testdir = tempfile.mkdtemp(prefix='unittest-')
        os.chdir(self.testdir)

    def teardown(self):
        os.chdir(self.cwd)
        shuil.rmtree(self.testdir, ignore_errors=True)

    def test_call(self):
        self.assertFalse(os.path.exists("FOOBAR"))
        xd.tool.shell.call("touch FOOBAR")
        self.assertTrue(os.path.exists("FOOBAR"))

    def test_call_true(self):
        self.assertTrue(xd.tool.shell.call("true"))

    def test_call_false(self):
        self.assertFalse(xd.tool.shell.call("false"))
