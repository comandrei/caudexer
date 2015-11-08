import requests
# from collections import namedtuple
from time import sleep
import xml.etree.ElementTree as ET
from .models import GoodReadsData
from dexer.settings import GOODREADS_KEYS
import random

# GoodReadsBook = namedtuple("GoodReadsBook", [
#     "gr_id", "nr_reviews", "nr_text_reviews", "pub_year", "pub_month", "pub_day",
#     "average_rating", "title", "authors", "author_id", "img", "small_img"
# ])


SEARCH_URL = "https://www.goodreads.com/search/index.xml"


def search(title):
    sleep(1) # api requires us to be nice
    response = requests.get(SEARCH_URL, data={"key": _get_key(), "q": title})
    if response.status_code != 200:
        print(response.status_code, response.content)
        return []

    content = ET.fromstring(response.content)

    search_tag = _get_child(content, "search")
    results_tag = _get_child(search_tag, "results")

    books = []
    for result in results_tag.getchildren():
        # print "\n\n\n\nResult", index
        # _debug_print(result)
        books.append(make_book(result))

    return books


def _get_key():
    return random.choice(GOODREADS_KEYS)[0]

def _debug_print(node, padding=""):
    print(padding, node.tag, node.text, node.attrib)
    padding += "    "
    for child in node.getchildren():
        _debug_print(child, padding)


def make_book(node):
    book_data = {}
    book_data["good_reads_id"] = _get_child_val(node, "id")
    book_data["nr_reviews"] = _get_child_val(node, "ratings_count")
    book_data["nr_text_reviews"] = _get_child_val(node, "text_ratings_count")
    book_data["pub_year"] = _get_child_val(node, "original_publication_year")
    book_data["pub_month"] = _get_child_val(node, "original_publication_month")
    book_data["pub_day"] = _get_child_val(node, "original_publication_day")
    book_data["average_rating"] = _get_child_val(node, "average_rating")
    book_info = _get_child(node, "best_book")
    book_data["title"] = _get_child_val(book_info, "title", "")[:300]
    author_data = _get_child(book_info, "author")
    book_data["authors"] = _get_child_val(author_data, "name")
    book_data["author_id"] = _get_child_val(author_data, "id")
    book_data["img"] = _get_child_val(book_info, "image_url")
    book_data["small_img"] = _get_child_val(book_info, "small_image_url")

    book = GoodReadsData.from_data(**book_data)
    return book


def _get_child(parent, tag_name):
    for child in parent.getchildren():
        if child.tag == tag_name:
            return child
    return None


def _get_child_val(parent, tag_name, default=None):
    for child in parent.getchildren():
        if child.tag == tag_name:
            return child.text
    return default
