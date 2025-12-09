"""Tests for Structural Patterns."""
import unittest
from patterns.structural import LoggerAdapter, OldLogger, make_bold, Facade


class TestAdapter(unittest.TestCase):
    def test_logger_adapter(self):
        old_logger = OldLogger()
        adapter = LoggerAdapter(old_logger)
        self.assertIsNotNone(adapter.log('test'))


class TestDecorator(unittest.TestCase):
    def test_bold_decorator(self):
        result = make_bold(lambda x: x)('test')
        self.assertTrue(result.startswith('<b>'))
        self.assertTrue(result.endswith('</b>'))


class TestFacade(unittest.TestCase):
    def test_facade(self):
        facade = Facade()
        result = facade.do_work()
        self.assertIn('Facade:', result)
        self.assertIn('A', result)
        self.assertIn('B', result)


if __name__ == '__main__':
    unittest.main()
