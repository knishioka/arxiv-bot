import logging
import math
from datetime import datetime
from urllib.parse import parse_qsl, urlencode, urlsplit

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format="[%(asctime)s > %(module)s:%(lineno)d %(levelname)s] =>  %(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)
logger = logging.getLogger()


class ArxivException(Exception):
    """Exception for ArxivScraper."""

    pass


class ArxivScraper(object):
    """Scraping arxiv."""

    baseURL = "https://arxiv.org/search/advanced"
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,"
        + " like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }

    def search_params(self, term, from_date, to_date, date_type="submitted_date", size=200, start=0):
        """Search Parameters.

        Args:
            term: Search Word.
            from_date: First day of the date interval.
            to_date: Last day of the date inverval.
            date_type: either submitted_date, submitted_date_first, or announced_date_first
            size: The number of articles.
            start: Page num.

        Returns:
            dict: Parameter dict.

        """
        return {
            "advanced": "",
            "terms-0-term": term,
            "terms-0-operator": "AND",
            "terms-0-field": "all",
            "classification-physics_archives": "all",
            "classification-include_cross_list": "include",
            "date-filter_by": "date_range",
            "date-from_date": from_date,
            "date-to_date": to_date,
            "date-date_type": date_type,
            "abstracts": "show",
            "start": start,
            "size": size,
            "order": date_type,
        }

    @staticmethod
    def str_to_float(string):
        """Convert string to float."""
        return float(str(string).replace(",", "").replace("(", "").replace(")", "").strip())

    @staticmethod
    def str_to_int(string):
        """Convert string to integer."""
        return int(ArxivScraper.str_to_float(string))

    @staticmethod
    def get_total_pages(total_no_of_items, items_per_page):
        """Get the number of pages in the search results."""
        return (
            math.ceil(float(ArxivScraper.str_to_int(total_no_of_items)) / ArxivScraper.str_to_int(items_per_page)) or 1
        )

    def current_page_number(self, url):
        """Get current page number."""
        start = self.str_to_int(self.get_url_query_dict(url)["start"])
        size = self.str_to_int(self.get_url_query_dict(url)["size"])
        return int(start / size) + 1

    def get_url_query_dict(self, url):
        """Convert query to dict."""
        return (
            dict(parse_qsl(urlsplit(url).query))
            if url
            not in (
                "",
                None,
            )
            else {}
        )

    def gen_url(self, url, **qs):
        """Generate search url."""
        uri = urlsplit(url)
        parsed_url = "{uri.scheme}://{uri.netloc}{uri.path}".format(uri=uri)
        parsed_url_qs = self.get_url_query_dict(url)
        parsed_url_qs.update(**qs)
        parsed_url_qstr = urlencode(parsed_url_qs)
        return f"{parsed_url}?{parsed_url_qstr}"

    def get_response(self, url):
        """Get search results."""
        rsp = requests.get(url, headers=self.headers, timeout=60)
        rsp.raise_for_status()
        error = ", ".join(
            [
                err.text.strip()
                for err in BeautifulSoup(rsp.text, "html.parser").findAll("div", {"class": "help is-warning"})
            ]
        )
        if error:
            raise ArxivException(error)
        return rsp

    def parse_page_info(self, responseObject: object) -> dict:
        """Get Page info."""
        soup = BeautifulSoup(responseObject.text, "html.parser")
        url_query_dict = self.get_url_query_dict(responseObject.url)
        totalResults = soup.find("h1", {"class": "title is-clearfix"}).text.strip()
        startIndex = int(url_query_dict["start"])
        if "your query returned no results" in totalResults.lower():
            totalPages = 1
        else:
            totalPages = self.get_total_pages(self.str_to_int(totalResults.split()[-2]), url_query_dict["size"])

        return dict(
            totalPages=totalPages,
            totalResults=totalResults,
            startIndex=startIndex,
            responseObject=responseObject,
        )

    def parse_items_by_url(self, url: str) -> list:
        """Parse items by url."""
        return self.parse_items(self.get_response(url))

    def parse_items(self, rsp: object) -> list:
        """Parse items."""
        soup = BeautifulSoup(rsp.text, "html.parser")
        url_query_dict = self.get_url_query_dict(rsp.url)
        itemElems = soup.findAll("li", {"class": "arxiv-result"})
        items = []
        for itemElemIndex, itemElem in enumerate(itemElems, 1):
            itemId = (
                itemElem.select("p a")[-1].get("onclick").strip().split("document.getElementById('")[1].split("-")[0]
            )
            itemTitle = itemElem.find(
                "p", attrs={"class": lambda e: e.startswith("title") if e else False}
            ).text.strip()
            itemSummary = (
                itemElem.find("span", attrs={"class": lambda e: e.startswith("abstract-full") if e else False})
                .text.strip()
                .split("\n        \u25b3")[0]
            )
            itemAuthors = [
                a.text
                for a in itemElem.find("p", attrs={"class": lambda e: e.startswith("authors") if e else False}).findAll(
                    "a"
                )
            ]
            itemCategories = [
                c.text
                for c in itemElem.find(
                    "div", attrs={"class": lambda e: e.startswith("tags is-inline-block") if e else False}
                ).findAll("span")
            ]
            itemUpdated = datetime.strptime(
                itemElem.find("p", {"class": "is-size-7"}).text.strip().replace("  ", "").split("\n")[0].split(";")[0],
                "Submitted %d %B, %Y",
            )
            itemPublished = datetime.strptime(
                itemElem.find("p", {"class": "is-size-7"}).text.strip().replace("  ", "").split("\n")[1],
                "originally announced %B %Y.",
            )
            items.append(
                dict(
                    id=itemId,
                    itemUpdated=itemUpdated.strftime("%d %B %Y"),
                    itemPublished=itemPublished.strftime("%B %Y"),
                    itemTitle=itemTitle,
                    itemSummary=itemSummary,
                    itemAuthors=itemAuthors,
                    itemPrimaryCategory=url_query_dict.get("terms-0-term"),
                    itemCategories=itemCategories,
                )
            )
        return items

    def search(self, start_date: str, end_date: str, category_id: str) -> dict:
        """Search articles."""
        data = []
        do_scraping = True
        start, size = (0, 200)
        prefix = f"[category_id:{category_id} | start_date:{start_date} | end_date:{end_date} ]"
        logger.info(f"Started Search By: {prefix}")
        while do_scraping:
            url = self.gen_url(
                self.baseURL,
                **self.search_params(
                    category_id, start_date, end_date, date_type="submitted_date", size=size, start=start
                ),
            )
            current_page_number = self.current_page_number(url)
            rsp = self.get_response(url)
            page_info = self.parse_page_info(rsp)
            do_scraping = current_page_number != page_info["totalPages"]
            start += size
            logger.info(
                f"\t{prefix} {page_info['totalResults']} | Page {current_page_number}/{page_info['totalPages']}"
            )
            data.extend(self.parse_items(rsp))
        logger.info(f"Completed Search By: {prefix} Extracted {len(data)} results")
        return data
