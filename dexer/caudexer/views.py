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

    unsorted_books = []
    for book in search_all(title):
        gr_data = book.goodreadsdata_set.all().order_by('-timestamp')
        gr = gr_data[0] if gr_data else None
        gb_data = book.googlebooksdata_set.all().order_by('-timestamp')
        gb = gb_data[0] if gb_data else None
        unsorted_books.append([book, gr, gb])

    sorted_books_with_rank = algorithm(unsorted_books)
    #must serialize them
    return JSONResponse(len(sorted_books_with_rank))
