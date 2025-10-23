from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('result/', views.result, name='result'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),

]
