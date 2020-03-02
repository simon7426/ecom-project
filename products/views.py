from django.shortcuts import render
from .models import Product
from django.views.generic import ListView,DetailView,CreateView

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

class ProductCreateView(CreateView):
    model = Product
    fields = ['name','description','image','price']

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)