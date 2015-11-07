import json
import os

from django.db import models

import amazon.api


class AmazonBook(models.Model):
    pass


def file_credentials(path="~/.caudexer.aws.json"):
    full_path = os.path.expanduser(path)
    with open(full_path, 'r') as fp:
        return json.loads(fp.read())


def search(get_credentials=file_credentials, **options):
    creds = get_credentials()
    api = amazon.api.AmazonAPI(**creds)
    options.setdefault('SearchIndex', 'Books')
    results = api.search(**options)
    for index, result_item in enumerate(results):
        yield result_item

