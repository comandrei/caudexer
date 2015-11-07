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
        if self.title == None:
            return "Book rating:{0:4} reviews:{1:4} avg_rat:{2:4} age:{3:4}".format(self.rating, self.no_reviews, self.avg_rating, self.age)

class TestRating(TestCase):

    def test_same_age_review_range(self):
        books = [Book(None, 3, 40, 2), Book(None, 4, 20, 1), 
                 Book(None, 2, 10, 3)]
        rank_books(books)
        for book in sorted(
                books, key=lambda book: book.rating, reverse=True):
            print(book)



