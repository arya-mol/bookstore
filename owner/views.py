from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, DeleteView, UpdateView
from owner.models import Books
from owner.forms import BookForm, OrderProcessForm
from customer.decorators import owner_permission_required
from django.utils.decorators import method_decorator
from customer.models import Orders
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.


# def book_list(request):
#     return render(request,'book_list.html')
@method_decorator(owner_permission_required, name="dispatch")
class BookList(ListView):
    model = Books
    context_object_name = "books"
    template_name = 'book_list.html'


# class BookList(View):
# def get(self,request,*args,**kwargs):
#     qs=Books.objects.all()
#     context={"books":qs}
#     return render(request,'book_list.html',context)

@method_decorator(owner_permission_required, name="dispatch")
class BookDetail(DetailView):
    model = Books
    context_object_name = "book"
    template_name = 'book_detail.html'
    pk_url_kwarg = "id"


# class BookDetail(View):
# def get(self,request,*args,**kwargs):
#     id=kwargs["id"]
#     qs=Books.objects.get(id=id)
#     context={"book":qs}
#     return render(request,'book_detail.html',context)

@method_decorator(owner_permission_required, name="dispatch")
class AddBook(CreateView):
    model = Books
    form_class = BookForm
    template_name = 'book_add.html'
    success_url = reverse_lazy("listbook")

    # class AddBook(View):
    # def get(self,request,*args,**kwargs):
    #     form=BookForm()  # instance/object creation/copy
    #     context={"form":form}
    #     return render(request,'book_add.html',context)
    #
    # def post(self,request,*args,**kwargs):
    #     # print(request.POST)
    #     form=BookForm(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"book has been added")
    #         return redirect('listbook')
    #     else:
    #         context={"form":form}
    #         messages.error(request,"book adding failed")
    #         return render(request, 'book_add.html', context)


@method_decorator(owner_permission_required, name="dispatch")
class BookChange(UpdateView):
    model = Books
    template_name = 'book_change.html'
    form_class = BookForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy("listbook")

    # def get(self,request,*args,**kwargs):
    #     id=kwargs["id"]
    #     qs=Books.objects.get(id=id)
    #     # form=BookForm(initial={"book_name":book["book_name"],"author":book["author"],"price":book["price"],"copies":book["copies"]})
    #     # dict={"book_name":qs.book_name,
    #     #       "author":qs.author,
    #     #       "price":qs.price,
    #     #       "copies":qs.copies
    #     #       }
    #     # form=BookForm(initial=dict)
    #     form=BookForm(instance=qs)
    #     context={"form":form}
    #     return render(request,'book_change.html',context)
    #
    # def post(self,request,*args,**kwargs):
    #     id=kwargs["id"]
    #     qs=Books.objects.get(id=id)
    #     form=BookForm(request.POST,instance=qs,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("listbook")
    #     else:
    #         context = {"form": form}
    #         return render(request, 'book_change.html', context)


@method_decorator(owner_permission_required, name="dispatch")
class BookDelete(DeleteView):
    model = Books
    template_name = "book_delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("listbook")

    # def get(self,*args,**kwargs):
    #     id=kwargs["id"]
    #     book=Books.objects.get(id=id)
    #     book.delete()
    #     return redirect("listbook")


class OwnerDashboard(ListView):
    model = Orders
    template_name = "owner_dashboard.html"

    def get(self, request, *args, **kwargs):
        new_orders = self.model.objects.filter(status="orderplaced")
        context = {"n_orders": new_orders}
        return render(request, self.template_name, context)


# | - template filter


class OrderDetails(DetailView):
    model = Orders
    template_name = "order_detail.html"
    context_object_name = "order"
    pk_url_kwarg = "o_id"


class OrderProcessView(UpdateView):
    model = Orders
    template_name = "order_process.html"
    form_class = OrderProcessForm
    success_url = reverse_lazy("dashboard")
    pk_url_kwarg = "id"

    def form_valid(self, form):
        self.object = form.save()
        expected_delivery_date=form.cleaned_data.get("expected_delivery_date")
        send_mail(
            'Book Order Conformation',
            'Your order will be delivered on' + str(expected_delivery_date),
            'aryamolchanjaplackal@gmail.com',
            ['aryamolbca2021@gmail.com'],
            fail_silently=False,
        )

        return super().form_valid(form)

