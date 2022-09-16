from django import forms
from django.forms import ModelForm
from owner.models import Books
from customer.models import Orders

class BookForm(ModelForm):
    class Meta:
        model=Books
        exclude=("active_status",)
        widgets={
            "book_name":forms.TextInput(attrs={"class":"form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "copies": forms.NumberInput(attrs={"class": "form-control"}),

            "image": forms.FileInput(attrs={"class": "form-control"})

        }
        # fields=["book_name","author","price","copies"]
        # fields="__all__"

    def clean(self):
        cleaned_data=super().clean()
        price=int(cleaned_data["price"])
        copies=int(cleaned_data["copies"])
        if price<0:
            print("value < 0")
            msg="invalid price"
            self.add_error("price",msg)
        if copies<0:
            msg="invalid copies"
            self.add_error("copies",msg)


class OrderProcessForm(ModelForm):
    class Meta:
        model=Orders
        fields=["status","expected_delivery_date"]

        widgets={
            "status":forms.Select(attrs={"class":"form-select"}),
            "expected_delivery_date":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }


# class BookForm(forms.Form):
#     book_name=forms.CharField()
#     author=forms.CharField()
#     price=forms.CharField()
#     copies=forms.CharField()





