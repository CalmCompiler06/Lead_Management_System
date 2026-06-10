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

    path('api/regions/',views.region_api,name='region_api'),
    path('api/regions/<int:regionid>/',views.region_detail_api,name='region_detail_api'),

    path('api/leads/',views.lead_api,name='lead_api'),
    path('api/leads/<int:leadid>/',views.lead_detail_api,name='lead_detail_api'),

    path(
    'api/products/create/',
    views.product_create_api,
    name='product_create_api'),

    path(
    'api/regions/create/',
    views.region_create_api,
    name='region_create_api'),

    path(
    'api/leads/create/',
    views.lead_create_api,
    name='lead_create_api'),

    path(
    'api/products/update/<int:productid>/',
    views.product_update_api,
    name='product_update_api'),

    path(
    'api/products/delete/<int:productid>/',
    views.product_delete_api,
    name='product_delete_api'),

    path(
    'api/regions/update/<int:regionid>/',
    views.region_update_api,
    name='region_update_api'),

    path(
    'api/regions/delete/<int:regionid>/',
    views.region_delete_api,
    name='region_delete_api'),

    path(
    'api/leads/update/<int:leadid>/',
    views.lead_update_api,
    name='lead_update_api'),

    path(
    'api/leads/delete/<int:leadid>/',
    views.lead_delete_api,
    name='lead_delete_api'),
 
]