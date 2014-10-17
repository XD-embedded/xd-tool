import xd.tool.log

import unittest
import sys
import os
import tempfile
import shutil
import sh
import configparser

class TestCase(unittest.case.TestCase):

    def setUp(self):
        self.restore = {}
        self.restore['sys.path'] = sys.path.copy()
        self.restore['cwd'] = os.getcwd()
        self.testdir = tempfile.mkdtemp(prefix='unittest-')
        os.chdir(self.testdir)
        self.restore['PWD'] = os.environ.get('PWD')
        os.environ['PWD'] = self.testdir
        self.restore['sys.modules'] = list(sys.modules)

    def tearDown(self):
        sys.path = self.restore['sys.path']
        os.chdir(self.restore['cwd'])
        if self.restore['PWD']:
            os.environ['PWD'] = self.restore['PWD']
        else:
            del os.environ['PWD']
        shutil.rmtree(self.testdir, ignore_errors=True)
        xd.tool.log.deinit()
        for module in list(sys.modules):
            if not module in self.restore['sys.modules']:
                del sys.modules[module]

    def setup_layer(self, name='layer', priority=None):
        os.makedirs(os.path.join(self.testdir, name))
        os.chdir(os.path.join(self.testdir, name))
        config = configparser.ConfigParser()
        config.add_section('layer')
        if priority is not None:
            config['layer']['priority'] = str(priority)
        with open('.xd', 'w') as f:
            config.write(f)
        sh.git.init()
        sh.git.add('.xd')
        sh.git.commit(m='initial commit')

    def setup_manifest(self,
                       manifest_layer=False, manifest_priority=1000,
                       layers={}):
        os.mkdir(os.path.join(self.testdir, 'manifest'))
        os.chdir(os.path.join(self.testdir, 'manifest'))
        config = configparser.ConfigParser()
        config.add_section('manifest')
        if manifest_layer:
            config.add_section('layer')
            config['layer']['priority'] = str(manifest_priority)
        if layers:
            config.add_section('priority')
            for layer, priority in layers.items():
                if priority:
                    config['priority'][layer] = str(priority)
        with open('.xd', 'w') as f:
            config.write(f)
        sh.git.init()
        sh.git.add('.xd')
        sh.git.commit(m='initial commit')
        for layer in layers:
            sh.git.submodule.add(os.path.join(self.testdir, layer), layer)
        os.environ['PWD'] = os.path.join(self.testdir, 'manifest')

    def add_layer_command(self, layer_path, command, source):
        layer_module = '.'.join(layer_path.split(os.sep))
        cwd = os.getcwd()
        os.chdir(os.path.join(self.testdir, 'manifest', layer_path))
        os.makedirs(os.path.join(layer_path, 'cmd'))
        config = configparser.ConfigParser()
        config.read('.xd')
        config['layer']['commands'] = layer_module + '.cmd'
        with open('.xd', 'w') as f:
            config.write(f)
        open(os.path.join(layer_path, '__init__.py'), 'w').close()
        open(os.path.join(layer_path, 'cmd', '__init__.py'), 'w').close()
        with open(os.path.join(layer_path, 'cmd', '%s.py'%(command)), 'w') as f:
            f.write(source)
        os.chdir(cwd)
