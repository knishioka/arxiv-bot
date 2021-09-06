import xml.etree.ElementTree as ET
from urllib import request


def query():
    url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=5"
    data = request.urlopen(url)
    root = ET.fromstring(data.read())
    return root
