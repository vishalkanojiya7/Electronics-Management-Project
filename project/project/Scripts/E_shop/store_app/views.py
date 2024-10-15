from django.shortcuts import render,redirect 
from store_app.models import Product,Categories,Filter_Price,Brand,Contact_us
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import razorpay
from .models import Order,OrderItem
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Product 


client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))


# Create your views here.
def home(request):
    product=Product.objects.filter(status='Publish')

    context={
        'product':product,
    }
    return render(request,'home.html',context)

def BASE(request):
    return render(request,'base.html')

def PRODUCT(request):
     
     categories=Categories.objects.all()
     filter_price=Filter_Price.objects.all()
     brand=Brand.objects.all()
     

     CATID= request.GET.get('categories')
     PRICE_FILTER_ID=request.GET.get('filter_price')
     BRANDID=request.GET.get('brand')
     PRICE_LOWTOHIGHID=request.GET.get('PRICE_LOWTOHIGH')
     
    

     
     if CATID:
         product=Product.objects.filter(categories=CATID,status='Publish')
     elif PRICE_FILTER_ID:
         product=Product.objects.filter(filter_price=PRICE_FILTER_ID,status='Publish')
     elif BRANDID:
         product=Product.objects.filter(brand=BRANDID,status='Publish')
     elif PRICE_LOWTOHIGHID:
         product=Product.objects.filter(status='Publish').order_by('price')

                 
     else:
         product=Product.objects.filter(status='Publish')

     
     context={
        'product':product,
        'categories':categories,
        'filter_price':filter_price,
        'brand':brand,
    }
     return render(request,'product.html',context)

def SEARCH(request):
     query=request.GET.get('query')
     product=Product.objects.filter(name__icontains=query)
     context={
        'product':product
     }
     return render(request,'search.html',context)

def PRODUCT_DETAIL_PAGE(request,id):
     prod = get_object_or_404(Product, id=id)
     context={
        'prod':prod,

     }

     return render(request,'singleproduct.html',context)

def CONTACT_PAGE(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        contact=Contact_us(
            name=name,
            email= email,
            subject=subject,
            message=message,



        )
        subject=subject
        message=message
        email_from= settings.EMAIL_HOST_USER
        try:
           send_mail(subject,message,email_from,['kanojiyav633@gmail.com'])
           contact.save()
           return redirect('home')
        except:
             return redirect('contact_page')

        
    return render(request,'contact.html')

def AUTH(request):
    return render(request,'auth.html')


def HandleRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer=User.objects.create_user(username,email,pass1)
        customer.first_name=first_name
        customer.last_name=last_name
        customer.save()
        return redirect('register')





        
    return render(request, 'auth.html')


def HandleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or any other page
        else:
            return redirect('login')
     
    return render(request,'auth.html')

def HandleLogout(request):
    logout(request)
    
    return render(request,'home.html')



@login_required(login_url="/login/")
def cart_add(request, id):
    product = get_object_or_404(Product, id=id)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart/cart_details.html')

def Check_out(request):
    amount_str=request.POST.get('amount')
    amount_float=float(amount_str)
    amount=int(amount_float)

    payment=client.order.create({
        "amount": amount, 
        "currency": "INR",
        "payment_capture":"1"
    })
    order_id=payment['id']
    context ={
        'order_id':order_id,
        'payment':payment,
    }
    return render(request,'cart/checkout.html',context)

def Place_order(request):
    if request.method == 'POST':
        uid=request.session.get('_auth_user_id')
        user=User.objects.get(id=uid)
        cart=request.session.get('cart')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country=request.POST.get('country')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        order_id=request.POST.get('order_id')
        payment=request.POST.get('payment')
        amount=request.POST.get('amount')

        context={
            'order_id':order_id,
        }
        order= Order(
             user= user,
             firstname=firstname,
             lastname=lastname,
             address=address,
             city =city,
             state=state,
             country=country,
             postcode=postcode,
             phone=phone,
             email=email,
             payment_id=order_id,
             amount=amount,

        )
        order.save()
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']

            total=a*b

            item=OrderItem(
                user=user,
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                total=total,

            )
            item.save()

    return render(request,'cart/placeorder.html',context)

@csrf_exempt
def Success(request):
    if request.method=="POST":
        a = request.POST
        order_id= ""
        for key, val in a.items():
            if key =='razorpay_order_id':
                order_id=val
                break

        user=Order.objects.filter(payment_id=order_id).first()
        user.paid=True
        user.save()
    return render(request,'cart/thank_you.html')

def Your_Order(request):
    uid=request.session.get('_auth_user_id')
    user=User.objects.get(id=uid)
    order=OrderItem.objects.filter(user=user)
    context={
        'order':order,
    }

    return render(request,'your_order.html',context)

def About(request):
    return render(request,'about.html')