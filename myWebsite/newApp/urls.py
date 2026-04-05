from django.urls import path
from . import views

app_name = 'newApp'

urlpatterns = [
    path('',views.app,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('product/<int:product_id>/',views.product_detail,name='product_detail'),
   
]