from django.test import TestCase

import pytest

from . import amazon

# Create your tests here.

def test_file_credentials():
    creds = amazon.file_credentials()
    assert len(creds) == 3


def test_connection():
    assert amazon.search_books(Keywords='Python')


@pytest.mark.django_db
def test_amazon_adapter():
    options = {'Keywords': 'Richest Man in Babylon'}
    products = amazon.search_books(**options)
    first_product = next(products)
    first_book = amazon.models.AmazonBook.from_product_api(
        first_product
    )
    first_book.save()
    assert amazon.models.AmazonBook.objects.count() == 1
