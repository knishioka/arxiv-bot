"""Search articles on arXiv."""
import feedparser

from .article import Article


def query(sort_by="lastUpdatedDate", sort_order="descending"):
    """Run query to get articles.

    Args:
        sort_by (str): either "lastUpdatedDate" or "submittedDate".
        sort_order (str): either "ascending" or "descending".

    Returns:
        `list` of `Article`

    """
    url = (
        "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=5"
        f"&sortBY={sort_by}&sortOrder={sort_order}"
    )
    data = feedparser.parse(url)
    return [Article(article_dict) for article_dict in data["entries"]]


if __name__ == "__main__":
    articles = query()
    for article in articles:
        print(article.title, article.published)
