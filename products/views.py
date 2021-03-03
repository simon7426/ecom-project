from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from django.http import JsonResponse

import json
import datetime

from taggit.models import Tag


def home(request):
    context = {'products':Product.objects,'title':"Home"}
    return render(request,'products/home.html',context)

class ProductListView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

class ProductDetailView(DetailView):
    model = Product

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name','description','image','price','tags']

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name','description','image','price','tags']

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        product = self.get_object()
        if(self.request.user == product.owner):
            return True
        return False

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'
    def test_func(self):
        product = self.get_object()
        if(self.request.user == product.owner):
            return True
        return False

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    products = Product.objects.filter(tags=tag)
    return render(request, 'products/product_tag_list.html', {"products": products, "tag": tag})

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False) 
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
    context = {'items':items,'order':order}
    return render(request,'products/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False) 
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
    context = {'items':items,'order':order}
    return render(request,'products/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    #print('Action: ',action)
    #print('Product: ',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    
    orderitem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if(action=='add'):
        orderitem.quantity = orderitem.quantity+1
    elif(action=='remove'):
        orderitem.quantity = orderitem.quantity-1
    elif(action=='delete'):
        orderitem.quantity = 0
    orderitem.save()
    
    if(orderitem.quantity<=0):
        orderitem.delete()

    return JsonResponse("item added",safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if(request.user.is_authenticated):
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        print(total,order.get_cart_totalwithvat())
        if(total == order.get_cart_totalwithvat()):
            order.complete = True
        order.save()

        if(order.shipping == True):
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                district=data['shipping']['district'],
                zipcode=data['shipping']['zipcode']
            )
    
    else:
        print('User not logged in')
    return JsonResponse('Payment Submitted',safe=False)