from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .search import search_all
from .algorithm import algorithm

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

    books = search_all(title)
    unsorted_books = []
    for book, data in books.items():
        gb, gr, amz = data
        unsorted_books.append([book, gb, gr, amz])

    sorted_books_with_rank = algorithm(unsorted_books)

    data = []
    for book, gb, gr, amz in sorted_books_with_rank:
        snippet = gb.snippet if gb else ""
        img = ((gb.img if gb else None) or
               (gr.img if gr else None) or
               (amz.small_image_url if amz else None))
        lang = gb.language if gb else None
        rank = 1
        pub_year = ((gr.pub_year if gr else None) or
                    (gb.publish_year if gb else None) or
                    (amz.publication_date.year if amz else None))

        result = {
            "id": book.id,
            "title": book.title,
            "description": snippet,
            "authors": book.authors.split(','),
            "isbn": book.isbn_13,
            "thumbnail": img,
            "language": lang,
            "ranking": rank,
            "publish_year": pub_year,
        }
        data.append(result)
    return JSONResponse(data)


