from xd.tool.layer import *

from case import *
import os
import configparser


class ManifestStub(object):

    def __init__(self, topdir, priority={}):
        self.topdir = topdir
        self.priority = priority

    def get_priority(self, layer):
        return self.priority.get(layer)


class tests(TestCase):

    def test_init_no_priority(self):
        os.mkdir('layer')
        config = configparser.ConfigParser()
        config.add_section('layer')
        with open(os.path.join('layer', '.xd'), 'w') as f:
            config.write(f)
        manifest = ManifestStub(self.testdir)
        layer = Layer(manifest, 'layer')

    def test_init_not_a_layer_1(self):
        os.mkdir('layer')
        config = configparser.ConfigParser()
        with open(os.path.join('layer', '.xd'), 'w') as f:
            config.write(f)
        manifest = ManifestStub(self.testdir)
        with self.assertRaises(NotALayer):
            layer = Layer(manifest, 'layer')

    def test_init_not_a_layer_2(self):
        os.mkdir('layer')
        manifest = ManifestStub(self.testdir)
        with self.assertRaises(NotALayer):
            layer = Layer(manifest, 'layer')

    def test_init_manifest_layer(self):
        config = configparser.ConfigParser()
        config.add_section('layer')
        with open('.xd', 'w') as f:
            config.write(f)
        manifest = ManifestStub(self.testdir)
        layer = Layer(manifest, '.')

    def test_priority(self):
        os.mkdir('layer')
        config = configparser.ConfigParser()
        config.add_section('layer')
        config['layer']['priority'] = '10'
        with open(os.path.join('layer', '.xd'), 'w') as f:
            config.write(f)
        manifest = ManifestStub(self.testdir)
        layer = Layer(manifest, 'layer')
        self.assertEqual(layer.priority(), 10)

    def test_no_priority(self):
        os.mkdir('layer')
        config = configparser.ConfigParser()
        config.add_section('layer')
        with open(os.path.join('layer', '.xd'), 'w') as f:
            config.write(f)
        manifest = ManifestStub(self.testdir)
        layer = Layer(manifest, 'layer')
        self.assertIsNone(layer.priority())
