from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from estoque import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('estoque/', include('estoque.urls')),  # Inclui as URLs do app estoque
    path('login/', auth_views.LoginView.as_view(template_name='estoque/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]