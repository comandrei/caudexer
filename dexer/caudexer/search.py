from . import googlebooks as gb
from . import goodreads as gr
from . import amazon as amz
from .models import CaudexerBook
# from collections import namedtuple

# CaudexerBook= namedtuple("CaudexerBook", ["title", "authors", "isbn_13", "gb", "gr"])
DEBUG = False

def search_all(title):
    print("Searching for {}".format(title).encode('utf-8'))
    gr_results = gr.search(title)
    if DEBUG:
        print("Goodreads has {} results".format(len(gr_results)).encode('utf-8'))
    gb_results = gb.search(title)
    if DEBUG:
        print("Google books has {} results".format(len(gb_results)).encode('utf-8'))
    amz_results = amz.search(title)
    if DEBUG:
        print("Amazon books has {} results".format(len(amz_results)).encode('utf-8'))

    books = {}

    for res in gb_results:
        if res.id:
            book = res.caudexer_book
        else:
            book = find_book_or_create(
                books, isbn_13=res.isbn_13, title=res.title, authors=res.authors,
                categories=res.categories
            )
            res.caudexer_book = book
            res.save()
        books[book] = [res, None, None]
        if DEBUG:
            print(book, book.title.encode('utf-8'))

    for res in gr_results:
        # gr no isbn :(
        if res.id:
            book = res.caudexer_book
        else:
            book = find_book_or_create(books, title=res.title, authors=res.authors)
            res.caudexer_book = book
            res.save()
        book_data = books.setdefault(book, [None, None, None])
        book_data[1] = res
        if DEBUG:
            print(book, book.title.encode('utf-8'))

    for res in amz_results:
        authors = serialize_authors(res.authors)
        book_options = dict(title=res.title,
                            authors=authors, isbn_13=res.isbn_13)
        book = find_book_or_create(books, **book_options)
        res.caudexer_book = book
        res.save()
        book_data = books.setdefault(book, [None, None, None])
        book_data[2] = res
        if DEBUG:
            print(book, book.title.encode('utf-8'))


    print("Books: {}".format(len(books)))
    # for b in books:
    #       print(b.title, b.authors, b.isbn_13, b.gb != None, b.gr != None)
    return books


def book_matches(result, title=None, authors=None, isbn_13=None):
    if result.isbn_13 and isbn_13 and result.isbn_13 == isbn_13:
        return True
    if result.title and title and result.title == title:
        if matches_authors(result.authors, authors):
            return True
    return False


def serialize_authors(authors):
    if not authors:
        return ""
    return ', '.join([
        ' '.join(author.split(" ")) for author in authors
    ])


def matches_authors(res_authors, authors):
    if not res_authors or not authors:
        return True
    author1 = ' '.join(res_authors.split())
    author2 = ' '.join(authors.split())
    return author1 == author2


def find_book_or_create(results, title=None, isbn_13=None, authors=None, categories=None):
    """
    :returns CaudexerBook()
    """
    book = None
    for item in results:
        if book_matches(item, title, authors, isbn_13):
            book = item

    if isbn_13:
        try:
            book = CaudexerBook.objects.get(isbn_13=isbn_13)
        except CaudexerBook.DoesNotExist:
            book = None

    if not book:
        try:
            book = CaudexerBook.objects.get(title=title, authors=authors)
        except CaudexerBook.DoesNotExist:
            book = None

    if not book:
        book = CaudexerBook()

    update_data_if_unavailable(
        book, title=title, isbn_13=isbn_13, authors=authors, categories=categories
    )

    return book


def update_data_if_unavailable(book, title=None, isbn_13=None, authors=None, categories=None):
    changed = False
    if title and not book.title:
        changed = True
        book.title = title
    if isbn_13 and not book.isbn_13:
        changed = True
        book.isbn_13 = isbn_13
    if authors and not book.authors:
        changed = True
        book.authors = authors
    if categories and not book.categories:
        changed = True
        book.categories = categories
    if changed:
        book.save()
