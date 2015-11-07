from . import googlebooks as gb
from . import goodreads as gr
from collections import namedtuple

CaudexerBook= namedtuple("CaudexerBook", ["title", "authors", "isbn_13", "gb", "gr"])

def search_all(title):
    print("Searching for {}".format(title))
    gr_results = gr.search(title)
    print("Goodreads has {} results".format(len(gr_results)))
    gb_results = gb.search(title)
    print("Google books has {} results".format(len(gb_results)))

    books = []

    for res in gb_results:
        book = CaudexerBook(
            title=res.title,
            authors=res.authors,
            isbn_13=res.isbn_13,
            gb=res,
            gr=None
        )
        books.append(book)

    for res in gr_results:
        # gr no isbn :(
        book = find_previous_result(books, title=res.title, authors=res.authors)
        if not book:
            book = CaudexerBook(
                title=res.title,
                authors=res.authors,
                isbn_13=None,
                gb=None,
                gr=res
            )
            books.append(book)
        else:
            books.remove(book)
            updated_book = book._replace(gr=res)
            books.append(updated_book)

    print("Books: {}".format(len(books)))
    for b in books:
          print(b.title, b.authors, b.isbn_13, b.gb != None, b.gr != None)
    return books


def find_previous_result(results, title=None, authors=None, isbn_13=None):
    for result in results:
        if result.isbn_13 and isbn_13 and result.isbn_13 == isbn_13:
            return result
        if result.title and title and result.title == title:
            if matches_authors(result.authors, authors):
                return result
    return None


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
