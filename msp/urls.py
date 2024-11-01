from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemListViewSet, ItemDetailViewSet

router = DefaultRouter()
router.register(r'items', ItemListViewSet, basename='item-list')
router.register(r'item/details', ItemDetailViewSet, basename='item-detail')

urlpatterns = router.urls