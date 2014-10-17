from xd.tool.manifest import *
from xd.tool.main import *

from case import *
import os
import sh
import configparser


class tests(TestCase):

    def test_init_not_in_manifest_1(self):
        with self.assertRaises(NotInManifest):
            manifest = Manifest(self.testdir)

    def test_init_not_in_manifest_2(self):
        config = configparser.ConfigParser()
        config.add_section('manifest')
        with open('.xd', 'w') as f:
            config.write(f)
        with self.assertRaises(NotInManifest):
            manifest = Manifest(self.testdir)

    def test_init_not_in_manifest_3(self):
        config = configparser.ConfigParser()
        config.add_section('manifest')
        sh.git.init()
        with self.assertRaises(NotInManifest):
            manifest = Manifest(self.testdir)

    def test_init_in_manifest_1(self):
        config = configparser.ConfigParser()
        config.add_section('manifest')
        with open('.xd', 'w') as f:
            config.write(f)
        sh.git.init()
        manifest = Manifest(self.testdir)
        self.assertEqual(manifest.topdir, self.testdir)

    def test_init_in_manifest_2(self):
        config = configparser.ConfigParser()
        config.add_section('manifest')
        with open('.xd', 'w') as f:
            config.write(f)
        sh.git.init()
        sh.git.add('.xd')
        sh.git.commit(m='initial commit')
        manifest = Manifest(self.testdir)
        self.assertEqual(manifest.topdir, self.testdir)

    def test_init_in_layer(self):
        self.setup_layer('layer', 10)
        self.setup_manifest(layers={'layer':None})
        manifest = Manifest(os.path.join(self.testdir, 'manifest', 'layer'))
        self.assertEqual(manifest.topdir,
                         os.path.join(self.testdir, 'manifest'))

    def test_manifest_priority_1(self):
        self.setup_layer('layer', 42)
        self.setup_manifest(layers={'layer':None})
        manifest = Manifest(os.path.join(self.testdir, 'manifest'))
        self.assertEqual(manifest.layers[0].priority(), 42)

    def test_manifest_priority_2(self):
        self.setup_layer('layer')
        self.setup_manifest(layers={'layer':43})
        manifest = Manifest(os.path.join(self.testdir, 'manifest'))
        self.assertEqual(manifest.layers[0].priority(), 43)

    def test_manifest_priority_3(self):
        self.setup_layer('layer', 44)
        self.setup_manifest(layers={'layer':45})
        manifest = Manifest(os.path.join(self.testdir, 'manifest'))
        self.assertEqual(manifest.layers[0].priority(), 45)
