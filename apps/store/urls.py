from django.urls import path
from apps.orders.views import get_store_order
from .views import get_store_inventory

urlpatterns = [
    path('<int:store_id>/orders/', get_store_orders, name='store-orders'),
    path('<int:store_id>/inventory/', get_store_inventory, name='store-inventory')
]