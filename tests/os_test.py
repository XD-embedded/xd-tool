from xd.tool.os import *
import unittest
from nose.tools import raises, with_setup

import os
import tempfile
import glob

class tests(unittest.case.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        self.testdir = tempfile.mkdtemp(prefix='unittest-')

    def tearDown(self):
        os.chdir(self.cwd)
        os.rmdir(self.testdir)

    def test_pushd(self):
        self.assertEqual(os.getcwd(), self.cwd)
        with pushd(self.testdir):
            self.assertEqual(os.getcwd(), self.testdir)
        self.assertEqual(os.getcwd(), self.cwd)

    def test_pushd_same(self):
        os.chdir(self.testdir)
        self.assertEqual(os.getcwd(), self.testdir)
        with pushd(self.testdir):
            self.assertEqual(os.getcwd(), self.testdir)
        self.assertEqual(os.getcwd(), self.testdir)

    def test_pushd_nonexistant(self):
        self.assertEqual(os.getcwd(), self.cwd)
        testdir = '/tmp/THIS_DIRECTORY_SHOULD_NOT_EXIST'
        self.assertFalse(os.path.exists(testdir))
        with self.assertRaises(OSError):
            with pushd(testdir):
                pass
        self.assertEqual(os.getcwd(), self.cwd)

    def test_pushd_cwd_nonexistant(self):
        cwd = tempfile.mkdtemp(prefix='unittest-')
        os.chdir(cwd)
        os.rmdir(cwd)
        with self.assertRaises(OSError):
            os.getcwd()
        with self.assertRaises(OSError):
            with pushd(self.testdir):
                self.fail('this should not be reached')
        with self.assertRaises(OSError):
            os.getcwd()

    def test_pushd_cwd_removed(self):
        cwd = tempfile.mkdtemp(prefix='unittest-')
        os.chdir(cwd)
        with self.assertRaises(OSError):
            with pushd(self.testdir):
                os.rmdir(cwd)
        self.assertEqual(os.getcwd(), self.testdir)
