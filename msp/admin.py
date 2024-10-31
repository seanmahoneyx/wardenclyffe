from django.contrib import admin
from .models import (
    Item, SalesRep, Employee, Terms, Tax, Account, Customer, Vendor,
    CustomerLocation, VendorLocation, Contact, CostListHead, CostListLine,
    PriceListHead, PriceListLine, ContractHead, ContractLine, DropShipHead,
    DropShipLine, ReleaseHead, ReleaseLine, PurchaseHead, PurchaseLine
)

# Register models
admin.site.register(Item)
admin.site.register(SalesRep)
admin.site.register(Employee)
admin.site.register(Terms)
admin.site.register(Tax)
admin.site.register(Account)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(CustomerLocation)
admin.site.register(VendorLocation)
admin.site.register(Contact)
admin.site.register(CostListHead)
admin.site.register(CostListLine)
admin.site.register(PriceListHead)
admin.site.register(PriceListLine)
admin.site.register(ContractHead)
admin.site.register(ContractLine)
admin.site.register(DropShipHead)
admin.site.register(DropShipLine)
admin.site.register(ReleaseHead)
admin.site.register(ReleaseLine)
admin.site.register(PurchaseHead)
admin.site.register(PurchaseLine)