from threaddit.search.client import INDEX_NAME, TEXT_FIELDS, ensure_index, get_es

VALID_TYPES = {"post", "comment", "thread", "user"}


def _highlight_text(hit):
    highlight = hit.get("highlight") or {}
    for field in TEXT_FIELDS:
        snippets = highlight.get(field)
        if snippets:
            return snippets[0]
    return None


def _source_result(hit):
    source = hit.get("_source") or {}
    return {
        "type": source.get("doc_type"),
        "id": source.get("id"),
        "score": hit.get("_score"),
        "highlight": _highlight_text(hit),
        "source": source,
    }


def search_content(query, doc_type=None, limit=20, offset=0):
    if not query or not query.strip():
        return {"query": query, "took": 0, "total": 0, "counts": {}, "results": []}
    if not ensure_index():
        raise RuntimeError("Elasticsearch is not available")

    filters = []
    if doc_type:
        if doc_type not in VALID_TYPES:
            raise ValueError("Invalid search type")
        filters.append({"term": {"doc_type": doc_type}})

    body = {
        "from": offset,
        "size": limit,
        "track_total_hits": True,
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": [
                                "title^4",
                                "name^5",
                                "username^5",
                                "content^2",
                                "description^3",
                                "bio",
                                "post_title^2",
                                "thread_name^2",
                            ],
                            "fuzziness": "AUTO",
                            "type": "best_fields",
                        }
                    },
                    {
                        "multi_match": {
                            "query": query,
                            "type": "phrase_prefix",
                            "fields": ["name^6", "username^6", "title^4", "content"],
                        }
                    },
                ],
                "minimum_should_match": 1,
                "filter": filters,
            }
        },
        "highlight": {
            "pre_tags": ["<mark>"],
            "post_tags": ["</mark>"],
            "fields": {field: {} for field in TEXT_FIELDS},
            "fragment_size": 160,
            "number_of_fragments": 1,
        },
        "aggs": {"by_type": {"terms": {"field": "doc_type", "size": 10}}},
    }
    response = get_es().search(
        index=INDEX_NAME,
        from_=body["from"],
        size=body["size"],
        track_total_hits=body["track_total_hits"],
        query=body["query"],
        highlight=body["highlight"],
        aggs=body["aggs"],
    )
    counts = {bucket["key"]: bucket["doc_count"] for bucket in response.get("aggregations", {}).get("by_type", {}).get("buckets", [])}
    total = response.get("hits", {}).get("total", {})
    total_value = total.get("value", 0) if isinstance(total, dict) else total
    return {
        "query": query,
        "took": response.get("took", 0),
        "total": total_value,
        "counts": counts,
        "results": [_source_result(hit) for hit in response.get("hits", {}).get("hits", [])],
    }
