from django.db import models


class CaudexerBook(models.Model):
    isbn_13 = models.CharField(null=True, blank=True, max_length=300, unique=True)
    title = models.CharField(null=True, blank=True, max_length=300)
    authors = models.CharField(null=True, blank=True, max_length=300)
    categories = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (("isbn_13", "title", "authors"),)

    @property
    def gb_data(self):
        if not hasattr(self, "_gb_data"):
            try:
                self._gb_data = self.googlebooksdata_set.all().order_by("-timestamp")[0]
            except IndexError:
                self._gb_data = None

        return self._gb_data

    @property
    def gr_data(self):
        if not hasattr(self, "_gr_data"):
            try:
                self._gr_data = self.goodreadsdata_set.all().order_by("-timestamp")[0]
            except IndexError:
                self._gr_data = None

        return self._gr_data

    @property
    def amazon_data(self):
        if not hasattr(self, "_amazon_data"):
            try:
                # should have a way to determine most recent
                self._amazon_data = self.amazonbook_set.all()[0]
            except IndexError:
                self._amazon_data = None

        return self._amazon_data


class AmazonBook(models.Model):
    caudexer_book = models.ForeignKey(CaudexerBook)
    price_and_currency = models.CharField(max_length=100)
    asin = models.CharField(max_length=100)
    sales_rank = models.IntegerField(null=True, blank=True)
    offer_url = models.URLField(null=True, max_length=200, blank=True)
    authors = models.CharField(null=True, max_length=200, blank=True)
    publisher = models.CharField(null=True, max_length=200, blank=True)
    isbn_13 = models.CharField(null=True, blank=True, max_length=300)
    eisbn = models.CharField(null=True, blank=True, max_length=300)
    binding = models.CharField(null=True, blank=True, max_length=300)
    languages = models.CharField(null=True, blank=True, max_length=300)
    edition = models.CharField(null=True, blank=True, max_length=300)
    title = models.CharField(null=True, blank=True, max_length=300)
    publication_date = models.DateField(null=True)
    pages = models.IntegerField(null=True, blank=True)
    large_image_url = models.URLField(null=True, max_length=200, blank=True)
    medium_image_url = models.URLField(null=True, max_length=200, blank=True)
    small_image_url = models.URLField(null=True, max_length=200, blank=True)

    @classmethod
    def from_product(cls, product):
        options = dict(
            price_and_currency=u'{} {}'.format(*product.price_and_currency),
            asin=product.asin,
            sales_rank=product.sales_rank,
            offer_url=product.offer_url,
            authors=', '.join(product.authors),
            publisher=product.publisher,
            isbn_13=('978' if len(product.isbn or '') == 10 else '') + (product.isbn or ''),
            eisbn=product.isbn,
            binding=product.binding,
            languages=', '.join(product.languages),
            edition=product.edition,
            title=(product.title or "")[:300],
            publication_date=product.publication_date,
            pages=int(product.pages or 0),
            large_image_url=product.large_image_url,
            medium_image_url=product.medium_image_url,
            small_image_url=product.small_image_url,
        )
        results = cls.objects.all().filter(**options)
        if results:
            return results[0]
        return cls(**options)


class GoogleBooksData(models.Model):
    caudexer_book = models.ForeignKey(CaudexerBook)
    timestamp = models.DateField(auto_now_add=True)

    google_book_id = models.CharField(max_length=100)
    title = models.CharField(null=True, blank=True, max_length=300)
    snippet = models.TextField(null=True, blank=True)
    authors = models.CharField(null=True, blank=True, max_length=300)
    small_img = models.CharField(null=True, blank=True, max_length=300)
    img = models.CharField(null=True, blank=True, max_length=300)
    isbn_13 = models.CharField(null=True, blank=True, max_length=300)
    average_rating = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    nr_reviews = models.IntegerField(null=True, blank=True)
    language = models.CharField(null=True, blank=True, max_length=300)
    page_count = models.IntegerField(null=True, blank=True)
    publish_year = models.IntegerField(null=True, blank=True)
    categories = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    @classmethod
    def from_data(cls, **data):
        results = GoogleBooksData.objects.all().filter(**data).order_by("-timestamp")
        if results:
            return results[0]
        return GoogleBooksData(**data)


class GoodReadsData(models.Model):
    caudexer_book = models.ForeignKey(CaudexerBook)
    timestamp = models.DateField(auto_now_add=True)

    good_reads_id = models.CharField(max_length=100)
    average_rating = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    nr_reviews = models.IntegerField(null=True, blank=True)
    nr_text_reviews = models.IntegerField(null=True, blank=True)
    pub_year = models.IntegerField(null=True, blank=True)
    pub_month = models.IntegerField(null=True, blank=True)
    pub_day = models.IntegerField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=300)
    authors = models.CharField(null=True, blank=True, max_length=300)
    author_id = models.IntegerField()
    small_img = models.CharField(null=True, blank=True, max_length=300)
    img = models.CharField(null=True, blank=True, max_length=300)

    @classmethod
    def from_data(cls, **data):
        results = GoodReadsData.objects.all().filter(**data).order_by("-timestamp")
        if results:
            return results[0]
        return GoodReadsData(**data)
