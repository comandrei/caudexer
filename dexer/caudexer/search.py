from . import googlebooks as gb
from . import goodreads as gr
from .models import CaudexerBook
# from collections import namedtuple

# CaudexerBook= namedtuple("CaudexerBook", ["title", "authors", "isbn_13", "gb", "gr"])

def search_all(title):
    print("Searching for {}".format(title))
    gr_results = gr.search(title)
    print("Goodreads has {} results".format(len(gr_results)))
    gb_results = gb.search(title)
    print("Google books has {} results".format(len(gb_results)))

    books = []

    for res in gb_results:
        authors = serialize_authors(res.authors)

        book = find_book_or_create(res.isbn_13, res.title, authors)
        update_data_if_unavailable(book, title=res.title, authors=authors, isbn_13=res.isbn_13)
        res.caudexer_book = book
        res.save()
        books.append(book)

    for res in gr_results:
        # gr no isbn :(
        authors = serialize_authors(res.authors)
        book = find_book_or_create(title=res.title, authors=authors)
        res.caudexer_book = book
        update_data_if_unavailable(book, title=res.title, authors=authors)
        res.save()
        if book not in books:
            books.append(book)

    print("Books: {}".format(len(books)))
    # for b in books:
    #       print(b.title, b.authors, b.isbn_13, b.gb != None, b.gr != None)
    return books


def find_previous_result(results, title=None, authors=None, isbn_13=None):
    for result in results:
        if result.isbn_13 and isbn_13 and result.isbn_13 == isbn_13:
            return result
        if result.title and title and result.title == title:
            if matches_authors(result.authors, authors):
                return result
    return None


def serialize_authors(authors):
    if not authors:
        return ""
    return ', '.join([
        ' '.join(author.split()) for author in authors
    ])


def matches_authors(res_authors, authors):
    if not res_authors or not authors:
        return True
    author1 = ' '.join(res_authors[0].split())
    author2 = ' '.join(authors[0].split())
    if author1 == author2:
        return True
    else:
        print("authors do not match {} {}".format(author1, author2))
        return False


def find_book_or_create(title=None, isbn_13=None, authors=None):
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
