import pytest
from script.deploy import deploy_zktitans


@pytest.fixture(scope="session")
def metadata_uri():
    return ""


@pytest.fixture(scope="function")
def titans(metadata_uri):
    return deploy_zktitans(metadata_uri)
