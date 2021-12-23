# arxiv-bot

## Search By Date Range and Search Query

```python
from arxiv_bot.arxiv_scraper import ArxivScraper
results = ArxivScraper().search(start_date='2012-02', end_date='2012-04', category_id='cs.AI')
```


## Search By URL

```python
from arxiv_bot.arxiv_scraper import ArxivScraper
url = "https://arxiv.org/search/?query=Peek+Arc+Consistency&searchtype=all&abstracts=show&order=submitted_date&size=200"
results = ArxivScraper().parse_items_by_url(url)
```


## To Get Html Response

```python
from arxiv_bot.arxiv_scraper import ArxivScraper
url = "https://arxiv.org/search/?query=Peek+Arc+Consistency&searchtype=all&abstracts=show&order=submitted_date&size=200"
rsp = ArxivScraper().get_response(url)
```


## Error handling if bad input

```python
from arxiv_bot.arxiv_scraper import ArxivScraper
results = ArxivScraper().search(start_date='2012-02-05', end_date='abcd', category_id='cs.AI')
```
