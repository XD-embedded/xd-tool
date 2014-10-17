from xd.tool.os import *

from case import *
import unittest
import os
import tempfile


class tests(TestCase):

    def setUp(self):
        super(tests, self).setUp()
        self.cwd = self.restore['cwd']
        os.chdir(self.cwd)

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
        with tempfile.TemporaryDirectory(prefix='unittest-') as cwd:
            os.chdir(cwd)
            os.rmdir(cwd)
            with self.assertRaises(OSError):
                os.getcwd()
            with self.assertRaises(OSError):
                with pushd(self.testdir):
                    self.fail('this should not be reached')
            with self.assertRaises(OSError):
                os.getcwd()
            os.mkdir(cwd)

    def test_pushd_cwd_removed(self):
        with tempfile.TemporaryDirectory(prefix='unittest-') as cwd:
            os.chdir(cwd)
            with self.assertRaises(OSError):
                with pushd(self.testdir):
                    os.rmdir(cwd)
            self.assertEqual(os.getcwd(), self.testdir)
            os.mkdir(cwd)
