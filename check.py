from itertools import product
import os, django
from django.http import request
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecom.settings")
django.setup()

from products.models import OrderItem,Product,Customer,Order
from apyori import apriori

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
print(len(association_results)) 
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

"""
for item in association_results:
    pair = item[0] 
    items = [x for x in pair]
    print("Rule: " + Product.objects.get(id=items[0]).name + " -> " + Product.objects.get(id=items[1]).name)

    print("Support: " + str(item[1]))

    print("Confidence: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
    print("=====================================")
"""
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

cur_customer = 1

ord_items = OrderItem.objects.all()

sold_items = [ord.product.id for ord in ord_items]
sold_items = set(sold_items)
print(len(sold_items))
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
    print(Product.objects.get(id=x[1]).name)





