from rest_framework import serializers
from .models import (
    Item, SalesRep, Employee, Terms, Tax, Account, Customer, Vendor,
    CustomerLocation, VendorLocation, Contact, CostListHead, CostListLine,
    PriceListHead, PriceListLine, ContractHead, ContractLine, DropShipHead,
    DropShipLine, ReleaseHead, ReleaseLine, PurchaseHead, PurchaseLine
)

class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item_name', 'item_type', 'is_active', 'category', 'division']


class ItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'customer_name', 'is_active']


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class VendorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'vendor_name', 'main_phone', 'is_active']


class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class SalesRepSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesRep
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'is_active']


class ContractHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractHead
        fields = ['id', 'reference_number', 'customer', 'begin_effective_date', 'end_effective_date', 'is_active']


class ContractLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractLine
        fields = ['id', 'contract', 'item', 'contract_quantity', 'price', 'purchased_quantity', 'sold_quantity']


class DropShipLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropShipLine
        fields = ['id', 'item', 'quantity', 'price', 'amount', 'tax', 'tax_amount']

class DropShipHeadSerializer(serializers.ModelSerializer):
    order_lines = DropShipLineSerializer(many=True, read_only=True, source='dropshipline_set')

    class Meta:
        model = DropShipHead
        fields = ['id', 'number', 'customer', 'date_created', 'sales_rep', 'total_amount', 'order_lines']


class PurchaseLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseLine
        fields = ['id', 'item', 'quantity', 'price', 'amount', 'tax', 'tax_amount']

class PurchaseHeadSerializer(serializers.ModelSerializer):
    purchase_lines = PurchaseLineSerializer(many=True, read_only=True, source='purchaseline_set')

    class Meta:
        model = PurchaseHead
        fields = ['id', 'number', 'vendor', 'date_created', 'category', 'total_amount', 'purchase_lines']