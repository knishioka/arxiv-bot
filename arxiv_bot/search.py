"""Search articles on arXiv."""
import feedparser

from .article import Article


def query(category="cs.AI", max_results=100, sort_by="lastUpdatedDate", sort_order="descending"):
    """Run query to get articles.

    Args:
        category (str): you can find category taxonomy in https://arxiv.org/category_taxonomy.
        max_results (int): the maximum number of results (<= 30,000).
        sort_by (str): either "lastUpdatedDate" or "submittedDate".
        sort_order (str): either "ascending" or "descending".

    Returns:
        `list` of `Article`

    """
    url = (
        f"https://export.arxiv.org/api/query?search_query=cat:{category}&max_results={max_results}"
        f"&sortBy={sort_by}&sortOrder={sort_order}"
    )
    data = feedparser.parse(url)
    return [Article(add_primary_category(article_dict)) for article_dict in data["entries"]]


def add_primary_category(article_dict):
    """Extract primary category from dict.

    Args:
        article_dict (str): article dict.

    Returns:
        dict
    """
    article_dict["primary_category"] = article_dict["arxiv_primary_category"]["term"]
    return article_dict


if __name__ == "__main__":
    articles = query()
    for article in articles:
        print(article.title, article.journal_ref, article.published, article.updated)
