from django.urls import path
from customer import views


urlpatterns=[
    path('home',views.customerHome.as_view(),name="custhome"),
    path("accounts/signup",views.SignUpview.as_view(),name="signup"),
    path('',views.SigninView.as_view(),name="signin"),
    path('accounts/signout',views.sign_out,name="signout"),
    path('customers/carts/item/add/<int:id>',views.AddToCart.as_view(),name='addtocart'),
    path('customers/carts/items',views.CartItems.as_view(),name="cartitems"),
    path('customers/carts/items/remove/<int:id>',views.RemoveCartItem.as_view(),name="removeitem"),
    path("customers/orders/add/<int:p_id>/<int:c_id>",views.OrderCreate.as_view(),name="order_create"),
    path("customers/orders",views.MyOrdersView.as_view(),name="myorders"),
    path("customers/orders/remove/<int:id>",views.cancell_order,name="cancelorder"),
    path("customer/profile/add",views.ProfileView.as_view(),name="profile"),
    path("customer/profile/view",views.ViewMyProfile.as_view(),name="viewprofile")
]