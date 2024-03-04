import httpx


def parse_link_header(raw_link_header: str) -> list[dict]:
    """Convert a link header to a list of dictionaries"""
    if not raw_link_header:
        return []
    links = raw_link_header.split(",")
    parsed_links = []
    for link in links:
        parts = link.split(";")
        parsed_link = {}
        for part in parts:
            part = part.strip()
            if part.startswith("<") and part.endswith(">"):
                parsed_link["iri"] = part
            else:
                k, v = part.split("=")
                parsed_link[k.strip()] = v.strip()
        parsed_links.append(parsed_link)
    return parsed_links


def get_supported_media_types(response: httpx.Response) -> set:
    """Get the list of media types supported at /collections/{collectionId}/items

    Relies on definition of self and alternate links in the response headers
    """
    links = parse_link_header(response.headers.get("link", ""))
    return {
        link.get("type", None).strip('"') for link in links if link.get("rel").strip('"') == "self" or link.get("rel").strip('"') == "alternate"
    }
