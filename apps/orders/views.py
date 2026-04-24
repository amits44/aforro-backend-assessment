from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Resoponse
from rest_framework import status
from .models import Orders, OrderItem
from apps.products.models import Products
from apps.store.models import Store,Inventory

@api_view(['POST'])
def create_order(request):
    store_id = request.data.get("store_id")
    items_list= request.data.get("items",[])

    if not store_id or not items_list:
        return Response(
            {"erorr":"store_id and items are required"},
            status= status.HTTP_400_BAD_REQUEST
        )
    try:
        store = Store.objects.get(id ="store_id")
    except Store.DoesNotExcept:
        return Response(
            {"erroe":"store was no found"},
            status = status.HTTP_404_NOT_FOUND
        )
    with transaction.atomic():
        order = Orders.objects.create(store=store, status="pending")

        can_fufill = True
        inventory_to_update =[]
        order_items_to_create= []

        for items in items_data:
            product_id = items.get('product_id')
            quantity_requested = items.get('quantity_requested',1)

            try:
                product= Products.objects.get(id =product_id)
            except Product.DoesNotExist:
                can_fulfill = False
                break

            order_items_to_create.append(
                OrderItem(order=order, product=product, quantity_requested=quantity_requested)
            )
            try:
                inventory = Inventory.objects.select_for_update().get(
                    store=store, 
                    product=product
                )
                
                if inventory.quantity < quantity_requested:
                    can_fulfill = False
                else:
                    inventory.quantity -= quantity_requested
                    inventory_to_update.append(inventory)
                    
            except Inventory.DoesNotExist:
                can_fulfill = False

        if order_items_to_create:
            OrderItem.objects.bulk_create(order_items_to_create)

        if can_fulfill:
            for inv in inventory_to_update:
                inv.save()
            order.status = 'CONFIRMED'
        else:
            order.status = 'REJECTED'
            
        order.save()

    response_data = {
        "order_id": order.id,
        "store_id": store.id,
        "status": order.status,
        "items": [
            {
                "product_id": order_item.product_id,
                "quantity_requested": order_item.quantity_requested
            } for order_item in order_items_to_create
        ]
    }
    
    return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def store_order(request,store_id):
    try:
        store= Store.objects.get(id= store_id)
    except Store.DoesNotExist:
        return response(
            {'error':'store does no exist'},
            status= status.HTTP_404_NOT_EXIST
        )
    orders = Order.objects.filter(store=store).prefetch_related('items')
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data, status= status.HTTP_200_OK)