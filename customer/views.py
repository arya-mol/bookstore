from django.shortcuts import render,redirect
from django.views.generic import View,ListView,CreateView,TemplateView
from customer.forms import UserRegistrationForm,LoginForm,OrderForm,ProfileForm
from django.contrib.auth import authenticate,login,logout
from owner.models import Books
from customer.decorators import sign_in_required
from django.utils.decorators import method_decorator
from customer.models import Carts,Orders,Profile
from django.db.models import Sum
from django.contrib import messages
from customer.filters import BookFilter
from django.urls import reverse_lazy
# Create your views here.
@method_decorator(sign_in_required,name="dispatch")
class customerHome(View):

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            books = Books.objects.all()
            f = BookFilter(request.GET, queryset=Books.objects.all())
            context = {"books": books, "filter": f}
            return render(request, "cust_index.html", context)
        else:
            return redirect("signin")


class SignUpview(View):
    def get(self,request,*args,**kwargs):
        form=UserRegistrationForm()
        context={"form":form}
        return render(request,"signup.html",context)
    def post(self,request,*args,**kwargs):
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"signup.html")
        else:
            context={"form":form}
            return render(request,"signup.html",context)

class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        context={"form":form}
        return render(request,'signin.html',context)
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                if request.user.is_superuser:
                    return redirect('listbook')
                else:
                    return redirect("custhome")
            else:
                context={"form",form}
                return render(request, 'signin.html', context)

def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

class AddToCart(View):
    def get(self,request,*args,**kwargs):
        id=kwargs["id"]
        book=Books.objects.get(id=id)
        user=request.user
        cart=Carts(user=user,item=book)
        cart.save()
        print("item has been added")
        return redirect("custhome")


class CartItems(ListView):
    model = Carts
    template_name = "cart_items.html"
    context_object_name = "items"
    # def get_queryset(self):
    #     return self.model.objects.filter(user=self.request.user)

    def get(self,request,*args,**kwargs):
        qs=self.model.objects.filter(user=self.request.user).exclude(status="cancelled")

        total_sum=qs.aggregate(Sum("item__price"))
        total=total_sum["item__price__sum"]
        context={"items":qs,"total":total}
        return render(request,self.template_name,context)

class RemoveCartItem(View):
    model=Carts
    def get(self,request,*args,**kwargs):
        id=kwargs["id"]
        cart=Carts.objects.get(id=id)
        cart.status="cancelled"
        cart.save()
        return redirect("custhome")


class OrderCreate(CreateView):
    model = Orders
    template_name = "customer_order.html"
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        p_id=kwargs.get("p_id")
        c_id=kwargs.get("c_id")
        form=OrderForm(request.POST)
        if form.is_valid():
            cart=Carts.objects.get(id=c_id)
            address=form.cleaned_data.get("address")
            book=Books.objects.get(id=p_id)
            user=request.user
            order=Orders(item=book,user=user,address=address)
            order.save()
            cart.status="orderplaced"
            cart.save()
            messages.success(request,"your order has been placed")
            return redirect("custhome")


@method_decorator(sign_in_required,name="dispatch")
class MyOrdersView(ListView):
    model = Orders
    context_object_name = "orders"
    template_name = "my_orders.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).exclude(status="cancel")


def cancell_order(request,*args,**kwargs):
    o_id=kwargs.get("id")
    order=Orders.objects.get(id=o_id)
    order.status="cancel"
    order.save()
    messages.success(request,"your order has been cancelled")
    return redirect("custhome")


class ProfileView(CreateView):
    model = Profile
    template_name = "add_profile.html"
    form_class = ProfileForm

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST,files=request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect("custhome")
        else:
            return render(request,self.template_name,{"form":form})


class ViewMyProfile(TemplateView):
    template_name = "my_profile.html"