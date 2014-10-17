import xd.tool.shell

from case import *
import os

class tests(TestCase):

    def test_call(self):
        self.assertFalse(os.path.exists("FOOBAR"))
        xd.tool.shell.call("touch FOOBAR")
        self.assertTrue(os.path.exists("FOOBAR"))

    def test_call_true(self):
        self.assertTrue(xd.tool.shell.call("true"))

    def test_call_false(self):
        self.assertFalse(xd.tool.shell.call("false"))
