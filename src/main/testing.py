"""Support for testing without a DB."""

from django.test.simple import DjangoTestSuiteRunner  # @UnresolvedImport

class DatabaselessTestRunner(DjangoTestSuiteRunner):
    """A test suite runner that does not set up and tear down a database."""

    def setup_databases(self):
        """Overrides DjangoTestSuiteRunner"""
        pass

    def teardown_databases(self, *args):
        """Overrides DjangoTestSuiteRunner"""
        pass
