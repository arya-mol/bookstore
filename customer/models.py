from django.db import models
from django.contrib.auth.models import User
from owner.models import Books

# Create your models here.
class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(Books,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    options=(
        ('incart','incart'),
        ('cancelled','cancelled'),
        ('order_placed','order_placed')
    )
    status=models.CharField(max_length=120,choices=options,default='incart')


class Orders(models.Model):
    item=models.ForeignKey(Books,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    address=models.CharField(max_length=120)
    options=(
        ("orderplaced","orderplaced"),
        ("dispatched","dispatched"),
        ("cancel","cancel"),
        ("intransit","intransit"),
        ("delivered","delivered")
    )

    status=models.CharField(max_length=120,choices=options,default="orderplaced")
    expected_delivery_date=models.DateField(null=True)


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="customer")
    address=models.TextField()
    phno=models.CharField(max_length=10)
    picture=models.ImageField(upload_to="images")
