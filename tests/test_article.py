from arxiv_bot.article import Article
from arxiv_bot.search import add_primary_category


def test_parse_article(article_dict):
    article = Article(add_primary_category(article_dict))
    assert article.title == "Article Title"
    assert article.summary == "Article Summary"
    assert article.author == "Author Name"
    assert article.link == "http://arxiv.org/abs/cs/000000v1"
    assert article.published == "2021-01-01T00:00:00Z"
    assert article.updated == "2021-02-01T00:00:00Z"
    assert article.primary_category == "cs.AI"
    assert article.journal_ref == "Journal Ref"
