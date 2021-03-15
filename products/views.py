from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from django.http import JsonResponse

import json
import datetime

from taggit.models import Tag
from apyori import apriori
from .recommendation import recommend


def recommend(request):
    itemlist = OrderItem.objects.all()
    head = -1
    flist = []
    tmp = []
    for item in itemlist:
        id = item.order.id
        pro = item.product.id
        if(head==-1):
            head=id
            tmp = []
            tmp.append(pro)
        elif(head!=id):
            flist.append(tmp)
            head=id
            tmp = []
            tmp.append(pro)
        else:
            tmp.append(pro)
    flist.append(tmp)
    association_rules = apriori(flist, min_support=0.0045, min_confidence=0.01, min_lift=2, min_length=2)
    association_results = list(association_rules)  
    #print(len(association_results)) 
    ret1 = []
    flag = {}
    for item in association_results:
        pair = item[0]
        items = [x for x in pair]
        for y in items:
            if(y in flag):
                continue
            else:
                ret1.append(y)
                flag[y]=1

    customer_product = {}
    customer = Customer.objects.all()
    cus_ids = [cus.id for cus in customer]
    #print(len(customer))
    for cus in cus_ids:
        user_order = Order.objects.filter(customer=cus)
        #print(len(user_order))
        user_product = []
        for ord in user_order:
            tmp = OrderItem.objects.filter(order=ord)
            tmp = list(tmp)
            for x in tmp:
                user_product.append(x.product.id)
        user_product = set(user_product)
        #print(len(user_product))
        customer_product[cus] = user_product
    n = len(cus_ids)
    similarity = {}
    for i in range(n):
        tmp1 = customer_product[cus_ids[i]]
        for j in range(i+1,n):
            tmp2 = customer_product[cus_ids[j]]
            tmpi = tmp1.intersection(tmp2)
            tmpu = tmp1.union(tmp2)
            similarity[(cus_ids[i],cus_ids[j])] = len(tmpi)/len(tmpu)
            similarity[(cus_ids[j],cus_ids[i])] = len(tmpi)/len(tmpu)

    cur_customer = request.user.customer.id

    ord_items = OrderItem.objects.all()

    sold_items = [ord.product.id for ord in ord_items]
    sold_items = set(sold_items)
    #print(len(sold_items))
    pro_proba = []
    for item in sold_items:
        if(item in customer_product[cur_customer]):
            continue
        sm_up = 0
        sm_down = 0
        for other_customer in cus_ids:
            if(cur_customer == other_customer):
                continue
            sm_down+=similarity[(cur_customer,other_customer)]
            if(item in customer_product[other_customer]):
                sm_up+=similarity[(cur_customer,other_customer)]
        pro_proba.append((sm_up/sm_down,item))
    pro_proba.sort(reverse=True)
    ret2 = []
    for x in pro_proba:
        ret2.append(x[1])

    vote = {}
    mark = max(len(ret2),len(ret1))
    for x in ret1:
        if(x in vote):
            vote[x]+=mark
        else:
            vote[x]=mark
        mark-=1

    mark = max(len(ret2),len(ret1))
    for x in ret2:
        if(x in vote):
            vote[x]+=mark
        else:
            vote[x]=mark
        mark-=1
    vote_sort = []
    for key,val in vote.items():
        vote_sort.append((val,key))
    vote_sort.sort(reverse=True)
    ret = []
    for x in vote_sort[0:15]:
        #print(x[1])
        ret.append(Product.objects.get(id=x[1]))
    
    context = {'products':ret,'title':"Home"}
    #print(request.user.id)
    #print(request.user.customer.id)
    return render(request,'products/recommend.html',context)

class ProductListView(ListView):
    paginate_by = 9
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