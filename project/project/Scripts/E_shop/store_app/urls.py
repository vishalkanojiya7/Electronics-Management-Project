"""
URL configuration for E_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('base/',views.BASE,name='base'),
    path('products/',views.PRODUCT,name='products'),
    path('search/',views.SEARCH,name='search'),
    path('product_details/<int:id>',views.PRODUCT_DETAIL_PAGE,name='product_detail'),
    path('contact/',views.CONTACT_PAGE,name='contact_page'),
    path('register/',views.HandleRegister,name='register'),
    path('logout/',views.HandleLogout,name='logout'),
    path('login/',views.HandleLogin,name='login'),


    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('cart/checkout/',views.Check_out,name='checkout'),
    path('cart/checkout/placeorder/',views.Place_order,name='place_order'),
    path('success',views.Success,name='success'),
    path('Your_Order',views.Your_Order,name='your_order'),
    path('about/',views.About,name='about')
   




] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
