from . import googlebooks as gb
from . import goodreads as gr
from . import amazon as amz
from .models import CaudexerBook
# from collections import namedtuple

# CaudexerBook= namedtuple("CaudexerBook", ["title", "authors", "isbn_13", "gb", "gr"])

def search_all(title):
    print("Searching for {}".format(title))
    gr_results = gr.search(title)
    print("Goodreads has {} results".format(len(gr_results)))
    gb_results = gb.search(title)
    print("Google books has {} results".format(len(gb_results)))
    amz_results = amz.search(title)
    print("Amazon books has {} results".format(len(amz_results)))

    books = {}

    for res in gb_results:
        book = find_book_or_create(books, isbn_13=res.isbn_13, title=res.title, authors=res.authors)
        update_data_if_unavailable(book, title=res.title, authors=res.authors, isbn_13=res.isbn_13)
        res.caudexer_book = book
        res.save()
        books[book] = [res, None, None]
        print(book, book.title)

    for res in gr_results:
        # gr no isbn :(
        book = find_book_or_create(books, title=res.title, authors=res.authors)
        res.caudexer_book = book
        update_data_if_unavailable(book, title=res.title, authors=res.authors)
        res.save()
        book_data = books.setdefault(book, [None, None, None])
        book_data[1] = res

    for res in amz_results:
        authors = serialize_authors(res.authors)
        book_options = dict(title=res.title,
                            authors=authors, isbn_13=res.isbn_13)
        book = find_book_or_create(books, **book_options)
        update_data_if_unavailable(book, **book_options)
        res.caudexer_book = book
        res.save()
        book_data = books.setdefault(book, [None, None, None])
        book_data[2] = res
        print(book, book.title)


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


def find_book_or_create(results, title=None, isbn_13=None, authors=None):
    """
    :returns CaudexerBook()
    """
    for book in results:
        if book_matches(book, title, authors, isbn_13):
            return book
    if isbn_13:
        qs = CaudexerBook.objects.filter(isbn_13=isbn_13)
        if qs:
            return qs[0]
    return CaudexerBook.objects.get_or_create(title=title, authors=authors)[0]


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
