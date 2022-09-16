import django_filters
from owner.models import Books

class BookFilter(django_filters.FilterSet):
    class Meta:
        model=Books
        fields={"book_name":["contains"],
                "author":["contains"],
                "price":["lt"]
                }