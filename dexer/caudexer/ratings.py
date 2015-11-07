import math


def rank_books(books):
    avg_age = 0
    no_books = len(books)

    for book in books:
        avg_age = avg_age + book.age
    avg_age = avg_age / no_books

    for book in books:
        score = max(book.avg_rating * book.no_reviews, 1)
        sign = -1 if book.avg_rating < 3 else 1
        if book.avg_rating == 3:
            sign = 0
        book.rating = round(math.log10(score) + (sign * book.age) / avg_age, 2)
