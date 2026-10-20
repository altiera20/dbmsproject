import logging

from elasticsearch import Elasticsearch
from threaddit.config import ELASTICSEARCH_INDEX, ELASTICSEARCH_URL

logger = logging.getLogger(__name__)

INDEX_NAME = ELASTICSEARCH_INDEX
TEXT_FIELDS = [
    "title",
    "content",
    "name",
    "description",
    "username",
    "bio",
    "thread_name",
    "post_title",
]

INDEX_BODY = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
            "analyzer": {
                "threaddit_text": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding"],
                }
            }
        },
    },
    "mappings": {
        "properties": {
            "doc_type": {"type": "keyword"},
            "id": {"type": "integer"},
            "title": {
                "type": "text",
                "analyzer": "threaddit_text",
                "fields": {"raw": {"type": "keyword", "ignore_above": 256}},
            },
            "content": {"type": "text", "analyzer": "threaddit_text"},
            "name": {
                "type": "text",
                "analyzer": "threaddit_text",
                "fields": {"raw": {"type": "keyword", "ignore_above": 256}},
            },
            "description": {"type": "text", "analyzer": "threaddit_text"},
            "username": {
                "type": "text",
                "analyzer": "threaddit_text",
                "fields": {"raw": {"type": "keyword", "ignore_above": 256}},
            },
            "bio": {"type": "text", "analyzer": "threaddit_text"},
            "thread_id": {"type": "integer"},
            "thread_name": {"type": "keyword"},
            "thread_logo": {"type": "keyword", "index": False},
            "user_id": {"type": "integer"},
            "user_name": {"type": "keyword"},
            "user_avatar": {"type": "keyword", "index": False},
            "post_id": {"type": "integer"},
            "post_title": {"type": "text", "analyzer": "threaddit_text"},
            "media": {"type": "keyword", "index": False},
            "logo": {"type": "keyword", "index": False},
            "avatar": {"type": "keyword", "index": False},
            "created_at": {"type": "date"},
            "subscriber_count": {"type": "integer"},
            "posts_count": {"type": "integer"},
            "comments_count": {"type": "integer"},
            "post_karma": {"type": "integer"},
            "comment_karma": {"type": "integer"},
            "user_karma": {"type": "integer"},
        }
    },
}

_client = None


def get_es():
    global _client
    if _client is None:
        _client = Elasticsearch(ELASTICSEARCH_URL, request_timeout=5)
    return _client


def es_available():
    try:
        return bool(get_es().ping())
    except Exception as exc:
        logger.warning("Elasticsearch ping failed: %s", exc)
        return False


def document_id(doc_type, entity_id):
    return f"{doc_type}-{entity_id}"


def ensure_index():
    if not es_available():
        return False
    client = get_es()
    if not client.indices.exists(index=INDEX_NAME):
        client.indices.create(
            index=INDEX_NAME,
            settings=INDEX_BODY["settings"],
            mappings=INDEX_BODY["mappings"],
        )
        logger.info("Created Elasticsearch index %s", INDEX_NAME)
    return True
