from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import ProductListView,ProductDetailView,ProductCreateView,ProductUpdateView,ProductDeleteView
urlpatterns = [
    path('',ProductListView.as_view(),name="home"),
    path('product/<int:pk>/',ProductDetailView.as_view(),name="product-detail"),
    path('product/new/',ProductCreateView.as_view(),name="product-create"),
    path('product/<int:pk>/update',ProductUpdateView.as_view(),name="product-update"),
    path('product/<int:pk>/delete',ProductDeleteView.as_view(),name="product-delete"),
    path(
        'product/tags/<slug:slug>/',views.tag_detail,
        name="product-tag-list",
    ),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),
]

if(settings.DEBUG):
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)