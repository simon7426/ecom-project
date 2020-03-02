from django.shortcuts import render
from .models import Product
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

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
    fields = ['name','description','image','price']

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name','description','image','price']

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