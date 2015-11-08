from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404

from .models import CaudexerBook
from .search import search_all
from .algorithm import algorithm, _basic_ranking

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def search(request):
    if request.method != 'GET':
        return JSONResponse("Should be GET.")
    title = request.GET.get("title", "")
    if not title:
        return JSONResponse("Must provide title")

    books, meta = search_all(title)
    unsorted_books = []
    for book, data in books.items():
        gb, gr, amz = data
        unsorted_books.append([book, gb, gr, amz])

    sorted_books_with_rank = algorithm(unsorted_books)

    data = []
    for book, gb, gr, amz, rank in sorted_books_with_rank:
        snippet = gb.snippet if gb else ""
        img = ((gb.img if gb else None) or
               (gr.img if gr else None) or
               (amz.large_image_url if amz else None))
        lang = gb.language if gb else None

        if amz and amz.publication_date:
            amz_pub_year = amz.publication_date.year 
        else:
            amz_pub_year = None
        pub_year = ((gr.pub_year if gr else None) or
                    (gb.publish_year if gb else None) or amz_pub_year)
        result = {
            "id": book.id,
            "title": book.title,
            "description": snippet,
            "authors": (book.authors or '').split(','),
            "isbn": book.isbn_13,
            "thumbnail": img,
            "language": lang,
            "ranking": rank,
            "publish_year": pub_year,
        }
        data.append(result)

    response = {
        "results": data,
    }
    response.update(meta)
    return JSONResponse(response)


@csrf_exempt
def detail(request):
    if request.method != 'GET':
        return JSONResponse("Should be GET.")
    book_id = request.GET.get("id", "")
    if not book_id:
        return JSONResponse("Must provide 'id'")

    book = get_object_or_404(CaudexerBook, id=book_id)
    data = _serialize_book_data(book)
    return JSONResponse(data)


@csrf_exempt
def compare(request):
    if request.method != 'GET':
        return JSONResponse("Should be GET.")
    book_ids = request.GET.get("ids", "")
    if not book_ids:
        return JSONResponse("Must provide 'ids' split by ','")
    try:
        ids = [int(id) for id in book_ids.split(',')]
    except:
        return JSONResponse("Invalid ids format.")

    books = [get_object_or_404(CaudexerBook, id=book_id) for book_id in ids]
    books_data = [_serialize_book_data(book) for book in books]

    if not "side_by_side" in request.GET:
        return JSONResponse(books_data)
    else:
        return JSONResponse(_side_to_side(books_data))


def _side_to_side(books_data):
    if not books_data:
        return []
    data = {}
    for key in books_data[0]:
        data[key] = [book.get(key, None) for book in books_data]
    return data


def _serialize_book_data(book):
    data = {
        "id": book.id,
        "isbn_13": book.isbn_13,
        "title": book.title,
        "authors": (book.authors or '').split(','),
        "categories": (book.categories or '').split(','),
        "ranking": _basic_ranking(book, book.gb_data, book.gr_data, book.amazon_data)
    }

    if book.gb_data:
        gb = book.gb_data
        gb_info = {
            "date_retrieved": gb.timestamp,
            "google_books_identifier": gb.google_book_id,
            "snippet": gb.snippet,
            "image_url": gb.img,
            "isbn_13": gb.isbn_13,
            "average_rating": gb.average_rating,
            "nr_reviews": gb.nr_reviews,
            "language": gb.language,
            "page_count": gb.page_count,
            "publish_year": gb.publish_year,
            "categories": gb.categories,
            "description": gb.description,
        }
        data["Google Books Info"] = gb_info

    if book.gr_data:
        gr = book.gr_data
        gr_info = {
            "date_retrieved": gr.timestamp,
            "goodreads_identifier": gr.good_reads_id,
            "average_rating": gr.average_rating,
            "nr_reviews": gr.nr_reviews,
            "nr_text_reviews": gr.nr_text_reviews,
            "publish_year": gr.pub_year,
            "publish_month": gr.pub_month,
            "publish_day": gr.pub_day,
            "image_url": gr.img,
        }
        data["GoodReads Info"] = gr_info

    return data
