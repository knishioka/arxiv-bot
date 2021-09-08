class Article:
    def __init__(self, article_dict):
        self.title = article_dict["title"]
        self.summary = article_dict["summary"]
        self.author = article_dict["author"]
        self.link = article_dict["link"]
        self.published = article_dict["published"]
        self.updated = article_dict["updated"]
