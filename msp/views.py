# from django.shortcuts import render
# from django.http.response import HttpResponse
from rest_framework import viewsets
from .models import Item
from .serializers import (
    ItemListSerializer, ItemDetailSerializer,
)

# def item_view(request):
#     return HttpResponse("simple view")

class ItemListViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    
    def get_serializer_class(self):
        return ItemListSerializer
    
class ItemDetailViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    
    def get_serializer_class(self):
        return ItemDetailSerializer