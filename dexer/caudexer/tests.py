from django.test import TestCase
# Create your tests here.
from .ratings import rank_books


class Book(object):
    def __init__(self, title, avg_rating, no_reviews, age):
        self.title = title
        self.avg_rating = avg_rating
        self.no_reviews = no_reviews
        self.age = age

    def __repr__(self):
        return "Book rating: {} reviews {} age {} rating: {}".format(self.avg_rating, self.no_reviews, self.age, self.rating)

class TestRating(TestCase):

    def test_same_age_review_range(self):
        books = [Book("3 avg 40 rev", 3, 40, 2), Book("Book2", 4, 20, 1), Book("Book3", 2, 10, 3)]
        rank_books(books)
        print(sorted(books, key=lambda book: book.rating, reverse=True))
