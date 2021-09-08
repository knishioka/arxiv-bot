import pytest


@pytest.fixture
def article_dict():
    return {
        "id": "http://arxiv.org/abs/cs/000000v1",
        "guidislink": True,
        "link": "http://arxiv.org/abs/cs/000000v1",
        "updated": "2021-02-01T00:00:00Z",
        "published": "2021-01-01T00:00:00Z",
        "title": "Article Title",
        "title_detail": {
            "type": "text/plain",
            "language": None,
            "base": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=5",
            "value": "Article Title",
        },
        "summary": "Article Summary",
        "summary_detail": {
            "type": "text/plain",
            "language": None,
            "base": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=5",
            "value": "Article Summary",
        },
        "authors": [{"name": "Author Name"}],
        "author_detail": {"name": "Author Name"},
        "author": "Author Name",
        "arxiv_comment": "Arxive Comment",
        "arxiv_journal_ref": "Journal Ref",
        "links": [
            {"href": "http://arxiv.org/abs/cs/000000v1", "rel": "alternate", "type": "text/html"},
            {"title": "pdf", "href": "http://arxiv.org/pdf/cs/000000v1", "rel": "related", "type": "application/pdf"},
        ],
        "arxiv_primary_category": {"term": "cs.AI", "scheme": "http://arxiv.org/schemas/atom"},
        "tags": [{"term": "cs.AI", "scheme": "http://arxiv.org/schemas/atom", "label": None}],
    }
