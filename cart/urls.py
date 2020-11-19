from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include
from cart import views
from django.conf.urls import url
from django.conf.urls import handler404

app_name = 'cart'

urlpatterns = [
    # path('',views.product,name="product"),
    path('', views.HomeView.as_view(), name='MyView'),
    path('checkout/',views.checkout.as_view(),name="checkout"),
    path('payment/<payment_op>/',views.payment.as_view(),name="payment"),
    path('product/<slug>/',views.ItemDetailView.as_view(), name='product'),
    path('add_item/<slug>/',views.add_item, name='add_item'),
    path('delete_item/<slug>/', views.delete_item, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove_qty/<slug>/', views.remove_qty, name='remove_qty'),
    path('order_details/', views.order_details.as_view(), name='order_details'),
    path('<slug:category_slug>/',views.categories, name="categories"),
    path('', views.categories, name='categories'),
    # path('wish_list/', views.wish_list, name="wish_list"),
    path('search',views.search, name="search"),
   ]




