import datetime

from arxiv_bot.arxiv_scraper import ArxivScraper


def main():
    """List updated articles."""
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=2)
    end_date = today - datetime.timedelta(days=1)
    articles = ArxivScraper().search(start_date=start_date, end_date=end_date, category_id="cs.AI")
    for article in articles:
        print(article["itemTitle"])
        print(", ".join(article["itemAuthors"]))
        print(f'https://arxiv.org/abs/{article["id"]}')


if __name__ == "__main__":
    main()
