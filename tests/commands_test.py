from xd.tool.main import *

from case import *
from unittest.mock import patch
import os


class tests(TestCase):

    def add_layer_dummy_command(self, layer, command):
        self.add_layer_command(layer, command, '''
parser_help="dummy help"
def add_arguments(parser):
    parser.add_argument('--foo', action='store_true')
    return
def run(args, manifest, env):
    print("this is %s command: foo=%%s"%%(args.foo))
'''%(command,))

    def test_cmd_noargs(self):
        self.setup_layer('layer', 10)
        self.setup_manifest(layers={'layer':None})
        self.add_layer_dummy_command('layer', 'foobar')
        self.assertIsNone(main(['xd', 'foobar']))
        self.assertRegex(sys.stdout.getvalue(),
                         'this is foobar command: foo=False')

    def test_cmd_witharg(self):
        self.setup_layer('layer', 10)
        self.setup_manifest(layers={'layer':None})
        self.add_layer_dummy_command('layer', 'foobar')
        self.assertIsNone(main(['xd', 'foobar', '--foo']))
        self.assertRegex(sys.stdout.getvalue(),
                         'this is foobar command: foo=True')

    @patch('sys.exit')
    def test_cmd_package_broken(self, sys_exit_mock):
        self.setup_layer('layer', 10)
        self.setup_manifest(layers={'layer':None})
        self.add_layer_dummy_command('layer', 'foobar')
        with open(os.path.join(self.testdir, 'manifest', 'layer',
                               'layer', 'cmd', '__init__.py'), 'w') as f:
            f.write('FOOBAR')
        with self.assertLogs('xd.tool.commands', level='WARNING') as log:
            self.assertIsNone(main(['xd', '-h']))
        self.assertRegex(log.output[0],
                         'failed to import commands package layer.cmd')
        assert sys_exit_mock.called

    def test_package_in_command_package_(self):
        self.setup_layer('layer', 10)
        self.setup_manifest(layers={'layer':None})
        self.add_layer_dummy_command('layer', 'foobar')
        pkgdir = os.path.join('layer', 'layer', 'cmd', 'pkg')
        os.mkdir(pkgdir)
        open(os.path.join(pkgdir, '__init__.py'), 'w').close()
        self.assertIsNone(main(['xd', 'foobar']))
        self.assertRegex(sys.stdout.getvalue(),
                         'this is foobar command: foo=False')

    @patch('sys.exit')
    def test_bad_command_1(self, sys_exit_mock):
        self.setup_layer('layer', 10)
        self.setup_manifest(layers={'layer':None})
        self.add_layer_command('layer', 'foobar', 'FOOBAR')
        with self.assertLogs('xd.tool.commands', level='WARNING') as log:
            self.assertIsNone(main(['xd', '-h']))
        assert sys_exit_mock.called
        self.assertRegex(log.output[0],
                         'failed to import layer.cmd command: foobar')
        self.assertNotRegex(sys.stdout.getvalue(), 'foobar')

    @patch('sys.exit')
    def test_bad_command_2(self, sys_exit_mock):
        self.setup_layer('layer', 10)
        self.setup_manifest(layers={'layer':None})
        self.add_layer_command('layer', 'foobar', '''
parser_help="dummy help"
def add_arguments(parser):
    parser.add_argument('--foo', action='store_true')
    return
''')
        with self.assertLogs('xd.tool.commands', level='WARNING') as log:
            self.assertIsNone(main(['xd', '-h']))
        assert sys_exit_mock.called
        self.assertNotRegex(sys.stdout.getvalue(), 'foobar')

    def test_command_without_help(self):
        self.setup_layer('layer', 10)
        self.setup_manifest(layers={'layer':None})
        self.add_layer_command('layer', 'foobar', '''
def add_arguments(parser):
    pass
def run(args, manifest, env):
    print("this is foobar command")
''')
        with self.assertLogs('xd.tool.commands', level='WARNING') as log:
            self.assertIsNone(main(['xd', 'foobar']))
        self.assertRegex(log.output[0], 'missing help text')
        self.assertRegex(sys.stdout.getvalue(), 'this is foobar command')
