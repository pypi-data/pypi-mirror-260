import os
import pytest
import httpx

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    pass


@pytest.fixture(scope="session")
def instance_url() -> str:
    try:
        load_dotenv()
    except NameError:
        pass
    return os.environ.get("INSTANCE_URL", "")


if os.getenv("CLIENT_OVERRIDDEN") != 'True':
    @pytest.fixture(scope="session")
    def http_client(instance_url: str) -> httpx.Client:
        with httpx.Client() as client:
            client.base_url = instance_url
            yield client


@pytest.fixture(scope="session", autouse=True)
def suite_props(record_testsuite_property, instance_url):
    record_testsuite_property("instance-url", instance_url)
