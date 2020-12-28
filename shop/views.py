from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import datetime

# Create your views here.

def index(request):

    return render(request, 'shop/index.html')

def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        contact = Contact(name=name, email=email, phone=phone, subject=subject, message= message)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False


def search(request):
    # query =
    return render (request, 'shop/search.html')



def productView(request):
    return render (request, 'shop/productView.html')
def about(request):
    return render (request, 'shop/about.html')



@csrf_exempt
def product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create ( customer=customer, complete=False )
        items = order.orderitem_set.all ()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render (request, 'shop/product.html',context)

@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create ( customer=customer, complete=False )
        items = order.orderitem_set.all ()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    print(cartItems) 
    for item in items:
        print(item.product.product_name)   
    products = Product.objects.all()
    context = {'items': items, 'products': products, 'cartItems': cartItems}
    return render (request, 'shop/checkout.html', context)



def blog(request):
    return render (request, 'shop/blog.html')
def services(request):
    return render (request, 'shop/services.html')
def signin(request):
    return render (request, 'shop/signin.html')
def signup(request):
    return render (request, 'shop/signup.html')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create ( customer=customer, complete=False )

    orderItem, created = OrderItem.objects.get_or_create(order= order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer    
        order, created = Order.objects.get_or_create ( customer=customer, complete=False )
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address= data['shipping']['address'],
                city= data['shipping']['city'],
                state= data['shipping']['state'],
                zipcode= data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in...')
    return JsonResponse('Payment complete!', safe=False)
