import json
import os

import amazon.api


from . import models


def file_credentials(path="~/.caudexer.aws.json"):
    full_path = os.path.expanduser(path)
    with open(full_path, 'r') as fp:
        return json.loads(fp.read())


def search(keywords):
    """
    :returns: *AmazonBook* models that match keywords
    """
    try:
        results = [models.AmazonBook.from_product(result)
                   for result in search_books(Keywords=keywords)]
    except Exception:
        results = []
    return results

def search_books(get_credentials=file_credentials, **options):
    """
    Yields book products that match search options
    """
    try:
        creds = get_credentials()
        api = amazon.api.AmazonAPI(**creds)
    except Exception as exc:
        print(exc)
        return []
    options.setdefault('SearchIndex', 'Books')
    results = api.search(**options)
    for index, result_item in enumerate(results):
        yield result_item

