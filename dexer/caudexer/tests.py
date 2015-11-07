from django.test import TestCase
from . import amazon

# Create your tests here.

def test_file_credentials():
    creds = amazon.file_credentials()
    assert len(creds) == 3


def test_connection():
    assert amazon.search(KeyWords='Python')
