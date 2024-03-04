from json import JSONDecodeError
import pytest
import httpx

from .utils import get_supported_media_types


def pytest_collection_modifyitems(items):
    # Run the collected test functions in order of conformance test number
    items[:] = sorted(items, key=lambda item: int(item.name.replace("test_ct", "")))


@pytest.fixture(scope="session")
def implemented_media_types() -> set:
    return {"application/geo+json", ...}


@pytest.fixture(scope="session")
def collections(http_client) -> list[dict]:
    response = http_client.get("/collections", headers={"Accept": "application/json"})
    try:
        collections = response.json().get("collections", [])
    except JSONDecodeError:
        collections = []
    return collections


@pytest.fixture(scope="session")
def filterable_resources(
    collections: list[dict], http_client: httpx.Client, implemented_media_types: set
) -> list[dict]:
    resources = []
    for collection in collections:
        # Check for supported media types
        response = http_client.get(f"/collections/{collection['id']}/items")
        supported_media_types = get_supported_media_types(response)
        media_types = supported_media_types.intersection(implemented_media_types)
        if media_types:
            media_type = media_types.pop()  # Only keep one of the supported media types for testing
        else:
            raise Exception(
                f"None of the media types supported at {collection['id']} have been implemented in this test suite."
            )
        resource = dict()
        resource["id"] = collection["id"]
        resource["url"] = f"/collections/{collection['id']}/items"
        resource["media_type"] = media_type
        resources.append(resource)
    return resources
