from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductAPI.as_view(), name='api_products'),
    path('products/<int:id>/', views.ProductDetailAPI.as_view()),

    path('regions/', views.RegionAPI.as_view(), name='api_regions'),
    path('regions/<int:id>/', views.RegionDetailAPI.as_view()),

    path('leads/', views.LeadAPI.as_view(), name='api_leads'),
    path('leads/<int:id>/', views.LeadDetailAPI.as_view()),
]