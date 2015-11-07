import math


def rank_books(books):
    avg_age = 0
    no_books = len(books)

    for book in books:
        avg_age = avg_age + book.age
    avg_age = avg_age / no_books

    for book in books:
        score = book.avg_rating * book.no_reviews
        sign = -1 if book.avg_rating < 2.5 else 1
        if book.avg_rating == 2.5:
            sign = 0
        book.rating = math.log10(score) + (sign * book.age) / avg_age
