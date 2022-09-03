"""Article class."""


class Article:
    """Article class."""

    def __init__(self, article_dict):
        """Parse article dict returned by feedparser."""
        self.title = article_dict["title"]
        self.summary = article_dict["summary"]
        self.author = article_dict["author"]
        self.link = article_dict["link"]
        self.published = article_dict["published"]
        self.updated = article_dict["updated"]
        self.primary_category = article_dict["primary_category"]
        self.categories = article_dict.get("categories")
        self.journal_ref = article_dict.get("arxiv_journal_ref")
