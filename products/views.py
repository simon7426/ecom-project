from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from django.http import JsonResponse

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
    context = {'items':items}
    return render(request,'products/cart.html',context)

def checkout(request):
    return render(request,'products/checkout.html')

def updateItem(request):
    return JsonResponse("item added",safe=False)