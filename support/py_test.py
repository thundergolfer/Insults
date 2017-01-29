import sys
import os
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    """ Command to run PyTest UnitTest """
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['-v']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

class UnitTest(PyTest):
    def initialize_options(self):
        os.environ['INSULTS_ENV'] = 'test'
        TestCommand.initialize_options(self)
        self.pytest_args = ['-v', 'tests/unit']
