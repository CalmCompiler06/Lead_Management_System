from django.urls import path
from leadapp import views

urlpatterns = [

    # ================= LOGIN / LOGOUT =================

    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ================= HOME DASHBOARD =================

    path('home/', views.home, name='home'),
    #path('',views.home_dashboard, name='home_dashboard'),
    path('dashboard/', views.home_dashboard, name='home_dashboard'),

    # ================= PRODUCTS =================

    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('products/bulk-upload/', views.product_bulk_upload, name='product_bulk_upload'),
    path('products/export/',views.export_products,name='export_products'),

    # ================= REGIONS =================

    path('regions/', views.region_list, name='region_list'),
    path('regions/add/', views.add_region, name='add_region'),
    path('regions/edit/<int:pk>/', views.edit_region, name='edit_region'),
    path('regions/delete/<int:id>/', views.delete_region, name='delete_region'),
    path('regions/bulk-upload/',views.region_bulk_upload,name='region_bulk_upload'),
    path('regions/export/',views.export_regions,name='export_regions'),

    # ================= LEADS =================

    path('leads/', views.lead_list, name='lead_list'),
    path('leads/add/', views.add_lead, name='add_lead'),
    path('lead/edit/<int:id>/', views.edit_lead, name='edit_lead'),
    path('lead/delete/<int:id>/', views.delete_lead, name='delete_lead'),
    path('leads/bulk-upload/',views.lead_bulk_upload,name='lead_bulk_upload'),
    path('leads/export/',views.lead_export,name='lead_export'),

    # ================= ANALYTICS =================

    path('lead-analytics/', views.lead_analytics, name='lead_analytics'),
    path('product-analytics/', views.product_analytics, name='product_analytics'),
    path('region-analytics/', views.region_analytics, name='region_analytics'),

]
