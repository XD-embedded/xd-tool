import xd.tool.log

import unittest
from nose.tools import raises, with_setup

import logging
import io


def test_double_deinit():
    xd.tool.log.init()
    xd.tool.log.deinit()
    xd.tool.log.deinit()

class tests(unittest.case.TestCase):

    def setUp(self):
        self.stream = io.StringIO()
        self.logger = logging.getLogger('foo')

    def tearDown(self):
        xd.tool.log.deinit()

    def test_log_debug_on(self):
        xd.tool.log.init(self.stream)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug('test debug')
        self.assertEqual(self.stream.getvalue(), 'foo: test debug\n')

    def test_log_debug_off(self):
        xd.tool.log.init(self.stream)
        self.logger.setLevel(logging.INFO)
        self.logger.debug('test debug')
        self.assertEqual(self.stream.getvalue(), '')

    def test_log_info(self):
        xd.tool.log.init(self.stream)
        self.logger.info('test info')
        self.assertEqual(self.stream.getvalue(), 'test info\n')

    def test_log_warning(self):
        xd.tool.log.init(self.stream)
        self.logger.warning('test warning')
        self.assertEqual(self.stream.getvalue(), 'WARNING: test warning\n')

    def test_log_error(self):
        xd.tool.log.init(self.stream)
        self.logger.error('test error')
        self.assertEqual(self.stream.getvalue(), 'ERROR: test error\n')

    def test_log_critical(self):
        xd.tool.log.init(self.stream)
        self.logger.critical('test critical')
        self.assertEqual(self.stream.getvalue(), 'CRITICAL: test critical\n')

    def test_log_exc_info(self):
        xd.tool.log.init(self.stream)
        try:
            assert False
        except:
            self.logger.info('test exception', exc_info=True)
        loglines = self.stream.getvalue().split('\n')
        self.assertEqual(loglines[0], 'test exception')
        self.assertEqual(loglines[1], 'Traceback (most recent call last):')
