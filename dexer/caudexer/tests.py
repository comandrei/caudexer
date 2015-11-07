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
    amazon_options = {'Keywords': 'Richest Man in Babylon'}
    products = amazon.search_books(**amazon_options)
    first_product = next(products)
    first_book = amazon.models.AmazonBook.from_product(
        first_product
    )
    book_options = {'isbn_13': '1234567', 'title': 'Python'}
    caudexer_book = amazon.models.CaudexerBook.objects.create(**book_options)
    first_book.caudexer_book = caudexer_book
    first_book.save()
    assert amazon.models.AmazonBook.objects.count() == 1


@pytest.mark.django_db
def test_search_view(client):
    response = client.get('/api/search/?title=python')
    
