import pytest
import httpx


@pytest.fixture(scope="module")
def successful_filter_execution_status_codes() -> list:
    return [200, 204]


@pytest.fixture(scope="module")
def unsuccessful_filter_execution_status_codes() -> list:
    return [400]


@pytest.fixture(scope="module")
def valid_queryable() -> str:
    return "valid"


@pytest.fixture(scope="module")
def invalid_queryable() -> str:
    return "invalid"


def test_ct4(http_client: httpx.Client, filterable_resources: list[dict]):
    """/conf/queryables-query-parameters/get-conformance
    Test Purpose
        Check that the API declares support for the conformance class
    Test Method
        Given:
            n/a
        When:
            the request for the Conformance Declaration is executed
                method: GET
                path: {apiURI}/conformance
                header: Accept: application/json
                authentication, if authentication credentials are provided
        Then:
            assert successful execution (status code is "200", Content-Type header is "application/json");
            assert that $.conformsTo is a string array that includes the value "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/queryables-query-parameters".
    """
    response = http_client.get("/conformance", headers={"Accept": "application/json"})
    assert response.status_code == 200, "/conformance did not return 200"
    assert response.headers.get("Content-Type") == "application/json"
    conforms_to = response.json().get("conformsTo")
    assert isinstance(conforms_to, list)
    assert (
        "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/queryables-query-parameters"
        in conforms_to
    )


def test_ct5(
    http_client: httpx.Client,
    filterable_resources: list[dict],
    valid_queryable: str,
    invalid_queryable: str,
    successful_filter_execution_status_codes: list,
    unsuccessful_filter_execution_status_codes: list,
):
    """/conf/queryables-query-parameters/query-param
    Test Purpose
        Check that query parameters for queryables is supported
    Test Method
        Given:
            test "get-queryables" was successful
            the list of collections
            the sample queryable of every collection
        When:
            a request for every filterable resource that supports filtering is executed and every queryable (queryable) with a valid value for the queryable ({valid-value})
                method: GET
                path: {apiURI}/collections/{collectionId}/items
                query parameters (before percent encoding): {queryable}={valid-value}
                header: Accept: {responseMediaType}
                authentication, if authentication credentials are provided
        Then:
            assert successful execution (the status code is in the list of acceptable status codes for a successful execution, Content-Type header is {responseMediaType});
            assert that each returned resource matches the filter.
        When:
            a request for every filterable resource that supports filtering is executed and every queryable (queryable) with a invalid value for the queryable ({invalid-value})
                method: GET
                path: {apiURI}/collections/{collectionId}/items
                query parameters (before percent encoding): {queryable}={invalid-value}
                header: Accept: {responseMediaType}
                authentication, if authentication credentials are provided
        Then:
            assert unsuccessful execution (the status code is in the list of acceptable status codes for an unsuccessful execution).
    """
    for resource in filterable_resources:
        media_type = resource["media_type"]
        headers = {"Accept": media_type}
        valid_params = {resource["queryable"]: "valid-value"}
        response = http_client.get(
            resource["url"], headers=headers, params=valid_params
        )
        assert response.status_code in successful_filter_execution_status_codes
        invalid_params = {resource["queryable"]: "[invalid-value]"}
        response = http_client.get(
            resource["url"], headers=headers, params=invalid_params
        )
        assert response.status_code in unsuccessful_filter_execution_status_codes
