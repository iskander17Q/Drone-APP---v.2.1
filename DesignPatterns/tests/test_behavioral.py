"""Tests for Behavioral Patterns."""
import unittest
from patterns.behavioral import Sorter, BubbleSort, PythonSort, Subject, PrintObserver, Light, Switch, SwitchOnCommand


class TestStrategy(unittest.TestCase):
    def test_bubble_sort(self):
        sorter = Sorter(BubbleSort())
        result = sorter.perform([3, 1, 2])
        self.assertEqual(result, [1, 2, 3])

    def test_python_sort(self):
        sorter = Sorter(PythonSort())
        result = sorter.perform([3, 1, 2])
        self.assertEqual(result, [1, 2, 3])


class TestObserver(unittest.TestCase):
    def test_observer_notification(self):
        subject = Subject()
        observer = PrintObserver()
        subject.attach(observer)
        self.assertIsNotNone(subject._observers)
        self.assertEqual(len(subject._observers), 1)


class TestCommand(unittest.TestCase):
    def test_command_execution(self):
        light = Light()
        switch = Switch()
        self.assertFalse(light.on)
        switch.store_and_execute(SwitchOnCommand(light))
        self.assertTrue(light.on)


if __name__ == '__main__':
    unittest.main()
