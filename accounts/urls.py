from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='accounts/logout.html'),name="logout"),
    path('profile/',views.profile,name="profile"),
    path('profile/update',views.update,name="update"),
    path('profile/cart',views.cart,name="cart"),
    path('profile/checkout',views.checkout,name="checkout"),    
]

if(settings.DEBUG):
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
