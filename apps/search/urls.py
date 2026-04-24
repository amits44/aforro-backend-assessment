from django.urls import path
from .views import search_products, suggest_products

urlpatterns = [
    path('products/', search_products, name='search-products'),
    path('suggest/', views.suggest_products, name='search-suggest'),
]