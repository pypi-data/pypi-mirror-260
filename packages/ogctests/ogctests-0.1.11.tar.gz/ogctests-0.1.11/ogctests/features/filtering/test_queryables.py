import re
from json import JSONDecodeError

import httpx

from .utils import parse_link_header


def test_ct1(http_client: httpx.Client):
    """/conf/queryables/get-conformance
    Test Purpose
        Check that the API declares support for the conformance class
    Test Method
        Given:
            n/a
        When:
            the request for the Conformance Declaration is executed
                method: GET
                path: {apiURI}/conformance
                authentication, if authentication credentials are provided
        Then:
            assert successful execution (status code is "200", Content-Type header is "application/json");
            assert that $.conformsTo is a string array that includes the value "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/queryables".
    """
    response = http_client.get("/conformance", headers={"Accept": "application/json"})
    assert response.status_code == 200, "Conformance endpoint did not return 200"
    assert response.headers.get("Content-Type") == "application/json", "Conformance endpoint did not return json"
    conforms_to = response.json().get("conformsTo")
    assert isinstance(conforms_to, list), "The conformsTo property is not an array"
    assert (
        "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/queryables"
        in conforms_to
    ), "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/queryables not listed in the conformsTo property."


def test_ct2(http_client: httpx.Client, filterable_resources: list[dict]):
    """/conf/queryables/get-queryables-uris
    Test Purpose
        Check that a link to the Queryables resource exists for every filterable resource
    Test Method
        Given:
            the list of filterable resources ({apiURI}/{pathToResource});
        When:
            a request is executed for every filterable resource
                method: HEAD (if HEAD results in a 405 response, use GET instead)
                path: {apiURI}/{pathToResource}
                header: Accept: application/json
                authentication, if authentication credentials are provided
        Then:
            assert successful execution (status code is "200");
            assert that the response includes a Link header with rel set to http://www.opengis.net/def/rel/ogc/1.0/queryables or [ogc-rel:queryables];
            store the href value as the Queryables URI for the filterable resource ({queryablesUri}).
    """
    assert filterable_resources
    headers = {"Accept": "application/json"}
    for resource in filterable_resources:
        response = http_client.head(resource["url"], headers=headers)
        if response.status_code == 405:
            response = http_client.get(resource["url"], headers=headers)
        assert response.status_code == 200, f"resource {resource['id']} could not be retrieved."
        links = parse_link_header(response.headers.get("link", ""))
        rel = "http://www.opengis.net/def/rel/ogc/1.0/queryables"
        altrel = "[ogc-rel:queryables]"
        queryables_uri = [
            link.get("href")
            for link in links
            if link.get("rel") == rel or link.get("rel") == altrel
        ]
        assert queryables_uri, "No link with relation [ogc-rel:queryables] or http://www.opengis.net/def/rel/ogc/1.0/queryables available in the link header"
        resource["queryables_uri"] = queryables_uri


def test_ct3(http_client: httpx.Client, filterable_resources: list[dict]):
    """/conf/queryables/get-queryables
    Test Purpose
        Check that the Queryables resource exists for every filterable resource
    Test Method
        Given:
            test "get-queryables-uris" was successful
            the list of Queryables URI for the filterable resource ({queryablesUri})
        When:
            the request for the Queryables page is executed for every filterable resource
                method: GET
                path: {queryablesUri}
                header: Accept: application/schema+json
                authentication, if authentication credentials are provided
        Then:
            assert successful execution (status code is "200", Content-Type header is "application/schema+json");
            assert that the value of the $schema member is "https://json-schema.org/draft/2019-09/schema" or "https://json-schema.org/draft/2020-12/schema"
            assert that the value of the $id member is "{queryablesUri}".
            assert that the value of the type member is "object".
            assert that $.properties is a non-empty object;
            assert that each member in $.properties has an object as its value and the object either includes type member or a format member whose value starts with geometry-;
            assert that the response is a valid JSON Schema;
            store the key of an arbitrary property with a type member as the sample queryable of the filterable resource;
            store the key of an arbitrary property of the object as the spatial queryable of the filterable resource, if the value of member is an object that includes no type member and a format member with a value geometry-{type} where {type} is one of "point", "multipoint", "linestring", "multilinestring", "polygon", "multipolygon", or "geometry";
            store the value of the additionalProperties member or true, if it is not provided.
    """
    assert filterable_resources
    for resource in filterable_resources:
        queryables_uri = resource.get("queryables_uri")
        assert queryables_uri, f"No queryables_uri for collection: {resource['id']}"
        response = http_client.get(
            url=queryables_uri, headers={"Accept": "application/schema+json"}
        )
        assert response.status_code == 200, f"collection: {resource['id']} did not respond with 200"
        assert response.headers.get("Content-Type") == "application/schema+json", f"collection: {resource['id']} did not return application/schema+json"
        try:
            data = response.json()
        except JSONDecodeError:
            raise AssertionError("JSON Schema not valid")
        expected_schemas = [
            "https://json-schema.org/draft/2019-09/schema",
            "https://json-schema.org/draft/2020-12/schema",
        ]
        assert data.get("$schema") in expected_schemas, f"$schema is not one of the expected schemas: {resource['id']}"
        assert data.get("$id") == queryables_uri, f"$id not in response body at collection: {resource['id']}"
        assert data.get("type") == "object", f"type property is not equal to 'object', at collection: {resource['id']}"
        properties = data.get("properties", [])
        assert len(properties) > 0, f"no properties given for collection: {resource['id']}"
        queryable = None
        spatial_queryable = None
        for prop_id, prop in properties.items():
            assert isinstance(prop, dict)
            keys = prop.keys()
            assert "type" in keys or "format" in keys, f"missing type and format on property {prop_id} for collection: {resource['id']}"
            if re.match(
                "geometry-(point|multipoint|linestring|multilinestring|polygon|multipolygon|geometry)",
                prop.get("format", ""),
            ):
                spatial_queryable = prop_id
            else:
                queryable = prop_id
        additional_properties = data.get("additionalProperties", True)
        resource["queryable"] = queryable
        resource["spatial_queryable"] = spatial_queryable
        resource["additional_properties"] = additional_properties
