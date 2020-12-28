from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("shop/about/", views.about, name="AboutUs"),
    path("shop/contact/", views.contact, name="ContactUs"),
    # path("shop/tracker/", views.tracker, name="TrackingStatus"),
    path("shop/search/", views.search, name="Search"),
    path("shop/products/<int:myid>", views.productView, name="productview"),
    path("shop/checkout/", views.checkout, name="checkout"),
    path("shop/signin/", views.signin, name="signin"),
    path("shop/signup/", views.signup, name="signup"),
    path("shop/services/", views.services, name="services"),
    path("shop/blog/", views.blog, name="blog"),
    path("shop/product/", views.product, name="product"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),


    # path("", views.index, name="ShopHome"),
]
