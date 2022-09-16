from django.db import models

# Create your models here.



class Books(models.Model):
    book_name=models.CharField(max_length=120,unique=True)
    author=models.CharField(max_length=120)
    price=models.PositiveIntegerField()
    copies=models.PositiveIntegerField()
    image=models.ImageField(upload_to="images",null=True,blank=True)
    active_status=models.BooleanField(default=True)

    def __str__(self):
        return self.book_name


# ORM queries

# print all book details available under 600
# books=Books.objects.filter(price__lt=600)
# books

# print all book details whoes price range 400 to 600
# books=Books.objects.filter(price__gte=100,price__lte=150)

# print details of mybook
# book=Books.objects.get(id=2)
# print(book.book_name,book.author,book.price,book.copies)

# print details of books whoes copies >100
# book=Books.objects.filter(copies__gt=100)

# print count of books whoes copies >100
# book=Books.objects.filter(copies__gt=100).count()

# print count of books whoes active status is true
# books=Books.objects.filter(active_status=True).count()

# print inactive book names
book_names=Books.objects.filter(active_status=False).values("book_name")
