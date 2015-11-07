from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .search import search_all

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
    return JSONResponse(search_all(title))
