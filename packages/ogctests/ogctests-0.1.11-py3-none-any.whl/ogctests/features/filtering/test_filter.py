import httpx
import enum
import pytest


@pytest.fixture(scope="module")
def successful_filter_execution_status_codes():
    return [200, 204]


@pytest.fixture(scope="module")
def unsuccessful_filter_execution_status_codes():
    return [400]


@pytest.fixture(scope="module")
def filter_langs():
    return [
        {"name": "cql2-text", "default": True},
        {"name": "cql2-json", "default": False},
    ]


def test_ct6(http_client: httpx.Client, successful_filter_execution_status_codes):
    """/conf/filter/get-conformance
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
            assert that $.conformsTo is a string array that includes the value "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/filter".
    """
    response = http_client.get("/conformance", headers={"Accept": "application/json"})
    assert response.status_code in successful_filter_execution_status_codes
    assert response.headers.get("Content-Type") == "application/json"
    conforms_to = response.json().get("conformsTo")
    assert isinstance(conforms_to, list)
    assert (
        "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/filter" in conforms_to
    )


def test_ct7(
    http_client: httpx.Client,
    filterable_resources: list[dict],
    filter_langs,
    successful_filter_execution_status_codes,
    unsuccessful_filter_execution_status_codes,
):
    """/conf/filter/filter-param
    Test Purpose
        Check that the query parameter filter is supported
    Test Method
        Given:
            test "get-queryables" was successful
            the list of filterable resources
            the sample queryable of every filterable resource
        When:
            a request for each resource that supports filtering is executed without a filter parameter
                method: GET
                path: {apiURI}/{pathToResource}
                header: Accept: {responseMediaType}
                authentication, if authentication credentials are provided
        Then:
            assert successful execution (the status code is in the list of acceptable status codes for a successful execution, Content-Type header is {responseMediaType});
            store the result as the unfiltered result of the resource.
        When:
            a request for each resource that supports filtering is executed with a valid filter expression
                method: GET
                path: {apiURI}/{pathToResource}
                query parameters (before percent encoding): filter-lang={filter-lang}&filter={filter-valid} where {queryable} in {filter-valid} is replaced by the sample queryable of the filterable resource
                header: Accept: {responseMediaType}
                authentication, if authentication credentials are provided
        Then:
            assert successful execution (the status code is in the list of acceptable status codes for a successful execution, Content-Type header is {responseMediaType});
            assert that each returned resource matches the filter expression.
        When:
            a request for each resource that supports filtering is executed with an invalid filter expression
                method: GET
                path: {apiURI}/{pathToResource}
                query parameters (before percent encoding): filter-lang={filter-lang}&filter={filter-invalid} where {queryable} in {filter-invalid} is replaced by the sample queryable of the filterable resource
                header: Accept: {responseMediaType}
                authentication, if authentication credentials are provided
        Then:
            assert unsuccessful execution (the status code is in the list of acceptable status codes for an unsuccessful execution).
    """
    assert filterable_resources
    for resource in filterable_resources:
        headers = {"Accept": resource["media_type"]}
        unfiltered_response = http_client.get(resource["url"], headers=headers)
        assert (
            unfiltered_response.status_code in successful_filter_execution_status_codes
        )
        resource["unfiltered_response"] = unfiltered_response
        queryable = resource["queryable"]
        for lang in filter_langs:
            params = {"filter-lang": lang, "filter": f"{queryable}=valid"}
            response = http_client.get(
                resource["url"], headers=headers, params=params
            )
            assert response.status_code in successful_filter_execution_status_codes
            data = response.json()
            for feature in data.get("features", []):
                assert feature.get(queryable, "") == queryable
            params = {"filter-lang": lang, "filter": f"{queryable}=invalid"}
            response = http_client.get(
                resource["url"], headers=headers, params=params
            )
            assert response.status_code in unsuccessful_filter_execution_status_codes


def test_ct8(http_client: httpx.Client, filterable_resources: list[dict]):
    """/conf/filter/filter-lang-default
    Test Purpose
        Check that the query parameter filter-lang default value is supported
    Test Method
        Given:
            test "get-queryables" was successful
            the list of filterable resources
            the queryables of every filterable resource
            the filter language {filter-lang} is the default filter language
        When:
            a request for each resource that supports filtering is executed with a valid filter expression
                method: GET
                path: {apiURI}/{pathToResource}
                query parameters (before percent encoding): filter={filter-valid} where {queryable} in {filter-valid} is replaced by the sample queryable of the collection
                header: Accept: {responseMediaType}
                authentication, if authentication credentials are provided
        Then:
            assert successful execution (the status code is in the list of acceptable status codes for a successful execution, Content-Type header is {responseMediaType});
            assert that each returned resource matches the filter expression.
        When:
            a request for each resource that supports filtering is executed with an invalid filter expression
                method: GET
                path: {apiURI}/{pathToResource}
                query parameters (before percent encoding): filter={filter-invalid} where {queryable} in {filter-invalid} is replaced by the sample queryable of the collection
                header: Accept: {responseMediaType}
                authentication, if authentication credentials are provided
        Then:
            assert unsuccessful execution (the status code is in the list of acceptable status codes for an unsuccessful execution).
    """
    for resource in filterable_resources:
        url = f"/collections/{resource['id']}/items"
        headers = {"Accept": "application/geo+json"}
        queryable = resource["queryable"]
        params = {"filter": f"{queryable['key']}='{queryable['value']}'"}
        response = http_client.get(url, headers=headers, params=params)
        assert response.status_code in [200, 204]
        assert response.headers.get("Content-Type") == "application/geo+json"
        data = response.json()
        for feature in data.get("features", []):
            assert feature.get(queryable["key"], "") == queryable["value"]
        invalid_params = {"filter": "ooga=booga"}
        invalid_response = http_client.get(url, headers=headers, params=invalid_params)
        assert invalid_response.status_code == 400


def test_ct9(http_client: httpx.Client, filterable_resources: list[dict]):
    """/conf/filter/expression-construction
    Test Purpose
        Check that unknown queryables are rejected, if this is declared in the Queryables resource
    Test Method
        Given:
            test "get-queryables" was successful
            the list of filterable resources, reduced to those where additionalProperties is false`
            the sample queryable of every filterable resource in the list
        When:
            a request for each resource is executed with a filter expression with an unsupported queryable
                method: GET
                path: {apiURI}/{pathToResource}
                query parameters (before percent encoding): filter-lang={filter-lang}&filter={filter-valid} where {queryable} in {filter-valid} is replaced by "this_is_not_a_queryable"
                header: Accept: {responseMediaType}
                authentication, if authentication credentials are provided
        Then:
            assert unsuccessful execution (the status code is in the list of acceptable status codes for an unsuccessful execution).
    """
    resources_with_additional_props = [
        resource
        for resource in filterable_resources
        if resource["additional_properties"]
    ]
    for resource in resources_with_additional_props:
        url = f"/collections/{resource['id']}/items"
        headers = {"Accept": "application/geo+json"}
        params = {"filter-lang": "cql2-text", "filter": "this_is_not_a_queryable"}
        response = http_client.get(url, headers=headers, params=params)
        assert response.status_code == 400


def test_ct10(http_client: httpx.Client, filterable_resources: list[dict]):
    """/conf/filter/filter-crs-wgs84
    Test Purpose
        Check that spatial predicates assume WGS84 by default
    Test Method
        Given:
            test "get-queryables" was successful
            the list of filterable resources with a spatial queryable
            the spatial queryable of each filterable resource
            the WGS84 bbox of the resources in each filterable resource
        When:
            a request for each filterable resource is executed with a filter expression with a spatial predicate
                method: GET
                path: {apiURI}/{pathToResource}
                query parameters (before percent encoding): filter-lang={filter-lang}&filter={bbox-filter} where {spatialQueryable} in {bbox-filter} is replaced by by the spatial queryable, {x1} is replaced by the west-bound longitude of the WGS84 bbox of the resource, {y1} by the south-bound latitude, {x2} by the east-bound longitude, and {y2} by the north-bound latitude
                header: Accept: {responseMediaType}
                authentication, if authentication credentials are provided
        Then:
            assert successful execution (the status code is in the list of acceptable status codes for a successful execution, Content-Type header is {responseMediaType}).
            assert that result contains the same features as the unfiltered result of the filterable resource.
        When:
            a request for each filterable resource with a filter expression with a spatial predicate
                method: GET
                path: {apiURI}/{pathToResource}
                query parameters (before percent encoding): filter-lang={filter-lang}&filter={bbox-filter} where {spatialQueryable} in {bbox-filter} is replaced by by the spatial queryable, {x1} is replaced by "1000000", {y1} by "1000000", {x2} by "2000000", and {y2} by "2000000"
                header: Accept: {responseMediaType}
                authentication, if authentication credentials are provided
        Then:
            assert unsuccessful execution (the status code is in the list of acceptable status codes for an unsuccessful execution).
    """
    for resource in filterable_resources:
        url = f"/collections/{resource['id']}/items"
        headers = {"Accept": "application/geo+json"}
        response = http_client.get(
            f"/collections/{resource['id']}", headers={"Accept": "application/json"}
        )
        bbox = response.json()["extent"]["spatial"]["bbox"]
        cql_query = """
          "op": "s_within",
          "args": [
            { "property": {} },
            { "bbox": {} }
        """.format(
            resource["spatial_queryable"], bbox
        )
        params = {
            "filter-lang": CQL2_FILTER_LANG.json,
            "filter": f"{resource['spatial_queryable']}={bbox}",
        }
