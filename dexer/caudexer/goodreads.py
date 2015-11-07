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
    return random.choice(GOODREADS_KEYS)

def _debug_print(node, padding=""):
    print(padding, node.tag, node.text, node.attrib)
    padding += "    "
    for child in node.getchildren():
        _debug_print(child, padding)


def make_book(node):
    gr_id = _get_child_val(node, "id")
    nr_reviews = _get_child_val(node, "ratings_count")
    nr_text_reviews = _get_child_val(node, "text_ratings_count")
    pub_year = _get_child_val(node, "original_publication_year")
    pub_month = _get_child_val(node, "original_publication_month")
    pub_day = _get_child_val(node, "original_publication_day")
    average_rating = _get_child_val(node, "average_rating")
    book_info = _get_child(node, "best_book")
    title = _get_child_val(book_info, "title")
    author_data = _get_child(book_info, "author")
    authors = _get_child_val(author_data, "name")
    author_id = _get_child_val(author_data, "id")
    img = _get_child_val(book_info, "image_url")
    small_img = _get_child_val(book_info, "small_image_url")

    book = GoodReadsData(
        good_reads_id=gr_id,
        nr_reviews=nr_reviews,
        nr_text_reviews=nr_text_reviews,
        pub_year=pub_year,
        pub_month=pub_month,
        pub_day=pub_day,
        average_rating=average_rating,
        title=title,
        authors=authors,
        author_id=author_id,
        img=img,
        small_img=small_img
    )
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
