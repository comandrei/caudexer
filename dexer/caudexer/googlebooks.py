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
        gb_id = item['id']
        snippet = item.get('searchInfo', {}).get('textSnippet', None)
        # if not snippet:
        #     print("no snippet")
        info = item['volumeInfo']
        authors = info.get('authors', [])
        categories = info.get('categories', [])
        # if not categories:
        #     print("no categories")
        description = info.get('description', None)
        # if not description:
        #     print("no desc")
        small_img = info['imageLinks']['smallThumbnail']
        img = info['imageLinks']['thumbnail']
        isbn_13 = get_isbn13(info.get('industryIdentifiers', None))
        average_rating = info.get("averageRating", None)
        nr_reviews = info.get("ratingsCount", None)
        language = info.get("language", "")
        title = info['title']
        page_count = info.get("pageCount", None)
        publish_year = info.get("publishDate", None)
        book = GoogleBooksData(
            google_book_id=gb_id,
            snippet=snippet,
            title=title,
            authors=', '.join(authors),
            small_img=small_img,
            img=img,
            isbn_13=isbn_13,
            average_rating=average_rating,
            nr_reviews=nr_reviews,
            language=language,
            page_count=page_count,
            publish_year=publish_year,
            categories=','.join(categories),
            description=description
        )

        books.append(book)
    return books


def get_isbn13(identifiers):
    if not identifiers:
        return None
    for identifier in identifiers:
        if identifier['type'] == 'ISBN_13':
            return identifier['identifier']

    return None
