import feedparser

from .article import Article


def query():
    url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=5"
    data = feedparser.parse(url)
    return [Article(article_dict) for article_dict in data["entries"]]
