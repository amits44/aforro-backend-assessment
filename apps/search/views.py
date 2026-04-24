from django.db.models import Q, Subquery, OuterRef, IntegerField
from django.db.models import Case, When, Value, IntegerField
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.products.models import Product
from apps.stores.models import Inventory
from .serializers import ProductSearchSerializer

@api_view(['GET'])
def search_products(request):
    queryset = Product.objects.select_related('category')
    query = request.GET.get('q')
    if query:
        search_filter = (
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__name__icontains=query)
        )
        queryset = queryset.filter(search_filter)

    category = request.GET.get('category')
    if category:
        queryset = queryset.filter(category__name__iexact=category)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    store_id = request.GET.get('store_id')
    in_stock = request.GET.get('in_stock', '').lower() == 'true'

    if store_id:
        inventory_sq = Inventory.objects.filter(
            product=OuterRef('pk'), 
            store_id=store_id
        ).values('quantity')[:1]
        
        queryset = queryset.annotate(
            store_quantity=Subquery(inventory_sq, output_field=IntegerField())
        )

        if in_stock:
            queryset = queryset.filter(store_quantity__gt=0)
            
    elif in_stock:
        queryset = queryset.filter(inventory_records__quantity__gt=0).distinct()

    sort_by = request.GET.get('sort', 'relevance')
    if sort_by == 'price':
        queryset = queryset.order_by('price')
    elif sort_by == '-price':
        queryset = queryset.order_by('-price')
    elif sort_by == 'newest':
        queryset = queryset.order_by('-id') 

    paginator = PageNumberPagination()
    paginator.page_size = 10

    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    serializer = ProductSearchSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def suggest_products(request):
    query = request.GET.get('q', '').strip()

    if len(query) < 3:
        return Response([])
    suggestions = Product.objects.filter(
        title__icontains=query
    ).annotate(
        match_type=Case(
            When(title__istartswith=query, then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
    ).order_by('match_type', 'title').values_list('title', flat=True)[:10]
    return Response(list(suggestions))