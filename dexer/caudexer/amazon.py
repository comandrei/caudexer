import json
import os

import amazon.api


from . import models


def file_credentials(path="~/.caudexer.aws.json"):
    full_path = os.path.expanduser(path)
    with open(full_path, 'r') as fp:
        return json.loads(fp.read())


def search(get_credentials=file_credentials, **options):
    """
    Yields book models that match search options
    """
    creds = get_credentials()
    api = amazon.api.AmazonAPI(**creds)
    options.setdefault('SearchIndex', 'Books')
    results = api.search(**options)
    for index, result_item in enumerate(results):
        yield models.AmazonBook.from_product_api(result_item)

