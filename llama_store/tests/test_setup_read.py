"""
Sets up the writable tests.

This is desinged to run before any of the writable tests are run.
"""

import importlib
import os

from fastapi.testclient import TestClient
import pytest


def pytest_configure():
    """
    Configure the attributes for the test
    """
    # The API token - this is created in one test and used in another
    pytest.api_token = None

    # The API client
    pytest.client = None
    pytest.readonly_client = None


class TestSetupWrite:
    """
    Test the user endpoints. Tests in this fixture start at 1.
    """

    @classmethod
    def setup_class(cls):
        """
        Sets up the tests by recreating the database and creating a test client
        """
        # Disable write mode
        os.environ["ALLOW_WRITE"] = "false"

        import main  # pylint: disable=import-outside-toplevel

        importlib.reload(main)  # reset module state

        # Import the app
        from main import app  # pylint: disable=import-outside-toplevel

        # Create a test client
        pytest.readonly_client = TestClient(app)

    @pytest.mark.order(1000)
    def test_we_are_setup(self):
        """
        Test that we are setup correctly
        """
        assert True
