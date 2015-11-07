import json
import requests
from pprint import pprint
from collections import namedtuple
from .models import GoogleBooksData

SEARCH_URL = "https://www.googleapis.com/books/v1/volumes"

# GoogleBook = namedtuple("GoogleBook", [
#     "gb_id", "title", "snippet", "authors", "small_img",
#     "img", "isbn_13", "average_rating", "nr_reviews", "language", "page_count", "publish_year"])

def search(title):
    response = requests.get(SEARCH_URL, params={"q": title, "maxResults": 40})
    if response.status_code != 200:
        print(response.status_code, response.content)
        return []

    results = response.json()
    # total_items = results['totalItems']
    items = results['items']
    books = []
    for item in items:
        book_data = {}
        book_data["google_book_id"] = item['id']
        book_data["snippet"] = item.get('searchInfo', {}).get('textSnippet', None)
        info = item['volumeInfo']
        book_data["authors"] = ', '.join(info.get('authors', []))
        book_data["categories"] = ', '.join(info.get('categories', []))
        book_data["description"] = info.get('description', None)
        book_data["small_img"] = info['imageLinks']['smallThumbnail']
        book_data["img"] = info['imageLinks']['thumbnail']
        book_data["isbn_13"] = get_isbn13(info.get('industryIdentifiers', None))
        book_data["average_rating"] = info.get("averageRating", None)
        book_data["nr_reviews"] = info.get("ratingsCount", None)
        book_data["language"] = info.get("language", "")
        book_data["title"] = info['title']
        book_data["page_count"] = info.get("pageCount", None)
        book_data["publish_year"] = info.get("publishDate", None)
        book = GoogleBooksData.from_data(**book_data)

        books.append(book)
    return books


def get_isbn13(identifiers):
    if not identifiers:
        return None
    for identifier in identifiers:
        if identifier['type'] == 'ISBN_13':
            return identifier['identifier']

    return None
