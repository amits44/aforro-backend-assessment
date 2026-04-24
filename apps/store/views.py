from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import StoreInventorySerializer

@api_view(['GET'])
def get_store_inventory(request, store_id):
    if not Store.objects.filter(id=store_id).exists():
        return Response(
            {'error':'store not found'},
            status=  status.HTTP_404_NOT_FOUND
        )
    inventory_items= Inventory.objects.filter(store_id=store_id).select_related('product','product_category').order_by('product_title')
    serializer = StoreInventorySerializer(inventory_items, many=True)
    return Response(serializer.data, status= status.HTTP_200_OK)
