

def algorithm(books_data):
    ranking_function = _basic_ranking
    computed = [
        [book, gb_data, gr_data, amz_data, ranking_function(book, gb_data, gr_data, amz_data)]
        for book, gb_data, gr_data, amz_data in books_data
    ]
    return sorted(computed, key=lambda data: data[4], reverse=True)


def _basic_ranking(book, gb_data, gr_data, amz_data):
    nr_reviews = 0.0
    total_rating_value = 0.0

    if gb_data and gb_data.nr_reviews and gb_data.average_rating:
        nr = float(gb_data.nr_reviews)
        nr_reviews += nr
        total_rating_value += (float(gb_data.average_rating) * nr)

    if gr_data and gr_data.nr_reviews and gr_data.average_rating:
        nr = float(gr_data.nr_reviews)
        nr_reviews += nr
        total_rating_value += (float(gr_data.average_rating) * nr)

    if total_rating_value == 0:
        return 0
    value = total_rating_value/nr_reviews
    return value
