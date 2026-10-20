#!/usr/bin/env python3
"""Rebuild the Elasticsearch index from PostgreSQL."""

from threaddit import app
from threaddit.search.indexer import reindex_all


def main():
    with app.app_context():
        count = reindex_all()
        print(f"Indexed {count} documents into Elasticsearch.")


if __name__ == "__main__":
    main()
