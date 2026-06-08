from django.urls import path
from . import views
from .views import product_api

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),

    path('regions/', views.region_list, name='region_list'),
    path('regions/add/', views.add_region, name='add_region'),
    path('regions/edit/<int:id>/', views.edit_region, name='edit_region'),
    path('regions/delete/<int:id>/', views.delete_region, name='delete_region'),

    path('leads/',views.lead_list,name='lead_list'),

    path('leads/add/',views.add_lead,name='add_lead'),
    path('leads/edit/<int:id>/',views.edit_lead,name='edit_lead'),

    path('leads/delete/<int:id>/',views.delete_lead,name='delete_lead'),

    path('api/products/',product_api,name='product_api'),
    path('api/products/<int:productid>/',views.product_detail_api,name='product_detail_api'),
]