from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('saint-raphael', views.senrafayel, name='senrafayel'),
    path('ferye', views.ferye, name='ferye'),
    path('grannrivye', views.grannrivye, name='grannrivye'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', views.signout, name='signout'),
    path('register/', views.register, name='register'),
]
