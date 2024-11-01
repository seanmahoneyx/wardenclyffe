from django.db import models
from django.utils import timezone
from django.db.models import Sum, F


### STATIC MODELS ###

class Item(models.Model):
    
    # CHOICES LISTS
    DIVISION_TYPES = [
        ('corrugated', 'Corrugated'),
        ('packaging', 'Packaging'),
        ('tooling', 'Tooling'),
        ('janitorial', 'Janitorial'),
        ('misc', 'Miscellaneous'),
    ]
    CATEGORY_TYPES = [
    ('5pf', '5PF'),
    ('angleboard', 'Angleboard'),
    ('bag', 'Bag'),
    ('bubble', 'Bubble'),
    ('chip', 'Chip'),
    ('chip_ptn', 'Chip Partition'),
    ('circle', 'Circle'),
    ('cup', 'Cup'),
    ('dc', 'D/C'),
    ('dcrsc', 'D/C RSC'),
    ('film', 'Film'),
    ('foam', 'Foam'),
    ('fol', 'FOL'),
    ('gloves', 'Gloves'),
    ('hsc', 'HSC'),
    ('label', 'Label'),
    ('litho', 'Litho'),
    ('misc', 'Miscellaneous'),
    ('other', 'Other'),
    ('pad', 'Pad'),
    ('parchwax', 'Parchment/Wax'),
    ('plastic_tray', 'Plastic Tray'),
    ('print', 'Print Plate'),
    ('ptn', 'Partition'),
    ('rsc', 'RSC'),
    ('sheet', 'Sheet'),
    ('sleeve', 'Sleeve'),
    ('slug', 'Slug'),
    ('ssc', 'SSC'),
    ('steel', 'Steel Die'),
    ('strapping', 'Strapping'),
    ('stretch', 'Stretch'),
    ('tape', 'Tape'),
    ('tele', 'Tele'),
    ('tray', 'Tray'),
    ('tube', 'Tube'),
    ('urn', 'Urn'),
    ]
    TEST_TYPES = [
        ('ect29', 'ECT 29'),
        ('ect32', 'ECT 32'),
        ('ect40', 'ECT 40'),
        ('ect44', 'ECT 44'),
        ('ect48', 'ECT 48'),
        ('ect51', 'ECT 51'),
        ('ect55', 'ECT 55'),
        ('ect112', 'ECT 112'),
        ('200t','200T'),
    ]
    FLUTE_TYPES = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
        ('e', 'E'),
        ('f', 'F'),
        ('bc', 'BC DW'),
        ('eb', 'EB DW'),
        ('tw', 'TW'),
    ]
    PAPER_TYPES = [
        ('k', 'Kraft'),
        ('mw', 'Mottled White'),
    ]
    ITEM_TYPES = [
        ('i', 'Inventory'),
        ('n', 'Non-Inventory'),
    ]
    
    item_name = models.CharField(unique=True, max_length=100)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    is_active = models.BooleanField(default=True)
    item_type = models.CharField(choices=ITEM_TYPES, max_length=30)
    revision = models.PositiveSmallIntegerField(blank=True, null=True)
    division = models.CharField(choices=DIVISION_TYPES, max_length=30)
    purch_desc = models.TextField(verbose_name="Purchase Description")
    sell_desc = models.TextField(verbose_name="Sell Description")
    category = models.CharField(choices=CATEGORY_TYPES, max_length=30)
    test = models.CharField(choices=TEST_TYPES, max_length=15)
    flute = models.CharField(max_length=6)
    paper = models.CharField(max_length=4)
    is_printed = models.BooleanField(default=False)
    panels_ptd = models.PositiveSmallIntegerField(blank=True, null=True)
    colors_ptd = models.PositiveSmallIntegerField(blank=True, null=True)
    ink_list = models.TextField()
    dim1 = models.DecimalField(max_digits=10, decimal_places=4)
    dim2 = models.DecimalField(max_digits=10, decimal_places=4)
    dim3 = models.DecimalField(max_digits=10, decimal_places=4)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    cogs_acct = models.ForeignKey('Account',blank=False, on_delete=models.SET_NULL, null=True, related_name='item_cogs_account')
    asset_acct = models.ForeignKey('Account',blank=False, on_delete=models.SET_NULL, null=True, related_name='item_asset_account')
    sale_acct = models.ForeignKey('Account',blank=False, on_delete=models.SET_NULL, null=True, related_name='item_sales_account')
    customer = models.ForeignKey('Customer',blank=False, on_delete=models.SET_NULL, null=True, related_name='item_customer')
    is_taxable = models.BooleanField(default=False, blank=False, null=False)
    tax = models.ForeignKey('Tax',blank=True, on_delete=models.SET_NULL, null=True, related_name='item_tax')
    
    
    def __str__(self):
        return self.item_name

class SalesRep(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Employee(models.Model):
    
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Terms(models.Model):
    name = models.CharField(unique=True, max_length=100, blank=False)
    net_due = models.PositiveSmallIntegerField()
    discount_percent = models.PositiveSmallIntegerField()
    discount_days = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Tax(models.Model):
    code = models.CharField(unique=True, max_length=20, blank=False)
    tax_percent = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
        ('Fixed', 'Fixed Asset'),
        ('Bank', 'Bank'),
        ('Loan', 'Loan'),
        ('Credit', 'Credit Card'),
        ('Equity', 'Equity'),
        ('AR', 'Accounts Receivable'),
        ('OCA', 'Other Current Asset'),
        ('Other Asset', 'Other Asset'),
        ('AP', 'Accounts Payable'),
        ('OCL', 'Other Current Liability'),
        ('LTL', 'Long Term Liability'),
        ('COGS', 'Cost of Goods Sold'),
        ('Other Income', 'Other Income'),
        ('Other Expense', 'Other Expense'),     
    ]
    
    is_active = models.BooleanField(default=True)
    account_type = models.CharField(max_length=50, blank=False)
    account_name = models.CharField(unique=True, max_length=100, blank=False)
    account_desc = models.TextField(blank=True)
    parent_account = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='account_subaccounts')

    def __str__(self):
        return self.account_name

class Customer(models.Model):
    customer_name = models.CharField(unique=True, max_length=100, blank=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    is_active = models.BooleanField(default=True)
    bill_street = models.CharField(max_length=100, blank=False)
    bill_pobox = models.CharField(max_length=100, blank=True)
    bill_city = models.CharField(max_length=60, blank=False)
    bill_state = models.CharField(max_length=2, blank=False)
    bill_zip = models.PositiveIntegerField(blank=False)
    main_phone = models.CharField(max_length=15, blank=True)
    main_email = models.EmailField(max_length=254, blank=True)
    ap_email = models.EmailField(max_length=254, blank=True)
    fax = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)
    credit_limit = models.PositiveIntegerField()
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.SET_NULL, null=True)
    csr = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='customer_csr')
    terms = models.ForeignKey(Terms, on_delete=models.SET_NULL, null=True, related_name='customer_terms')
    tax_code = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, related_name='customer_tax_code')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return self.customer_name

class Vendor(models.Model):
    vendor_name = models.CharField(unique=True, max_length=100, blank=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    is_active = models.BooleanField(default=True)
    bill_street = models.CharField(max_length=100, blank=True)
    bill_pobox = models.CharField(max_length=100, blank=True)
    bill_city = models.CharField(max_length=60, blank=True)
    bill_state = models.CharField(max_length=2, blank=True)
    bill_zip = models.PositiveIntegerField(blank=True)
    main_phone = models.CharField(max_length=15, blank=True)
    main_email = models.EmailField(max_length=254, blank=True)
    ar_email = models.EmailField(max_length=254, blank=True)
    fax = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)
    credit_limit = models.PositiveIntegerField()
    check_name = models.CharField(max_length=150, blank=True)
    tax_id = models.CharField(max_length=20, blank=True)
    is_1099 = models.BooleanField(default=False, blank=False)
    terms = models.ForeignKey(Terms, on_delete=models.SET_NULL, null=True, related_name='vendor_terms')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return self.vendor_name

class CustomerLocation(models.Model):
    is_active = models.BooleanField(default=True)    
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)   
    location_name = models.CharField(max_length=100, unique=True)
    street = models.CharField(max_length=100, blank=False)
    pobox = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=60, blank=False)
    state = models.CharField(max_length=2, blank=False)
    zip = models.PositiveIntegerField(blank=False)
    contact_name = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, related_name="customer_location_contact_name")
    contact_phone = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, related_name="customer_location_contact_phone")
    contact_email = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, related_name="customer_location_contact_email")
    delivery_open = models.TimeField()
    delivery_close = models.TimeField()
    is_boxtruck_able = models.BooleanField(default=True, null=False, blank=False)
    is_trailer_able = models.BooleanField(default=True, null=False, blank=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer} {self.location_name}"
    
    @property
    def contact_full_name(self):
        if self.contact:
            return f"{self.contact.first_name} {self.contact.last_name}"
        return "No Contact Assigned"
    
class VendorLocation(models.Model):
    is_active = models.BooleanField(default=True)    
    vendor = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)   
    location_name = models.CharField(max_length=100, unique=True)
    street = models.CharField(max_length=100, blank=False)
    pobox = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=60, blank=False)
    state = models.CharField(max_length=2, blank=False)
    zip = models.PositiveIntegerField(blank=False)
    contact_name = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, related_name="vendor_location_contact_name")
    contact_phone = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, related_name="vendor_location_contact_phone")
    contact_email = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, related_name="vendor_location_contact_email")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.vendor} {self.location_name}"
    
    @property
    def contact_full_name(self):
        if self.contact:
            return f"{self.contact.first_name} {self.contact.last_name}"
        return "No Contact Assigned"
    
class Contact(models.Model):
    CONTACT_TYPES = [
        ('v', 'Vendor'),
        ('c', 'Customer'),
        ('o', 'Other'),
    ]

    type = models.CharField(max_length=10, choices=CONTACT_TYPES, null=False, blank=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


############ DYNAMIC MODELS ##################

#TODO
# Transaction models
# NONPOSTING- Sales Order, Purchase Order, Quote, Blanket, Contract 
# POSTING- Invoice, Bill, Item Receipt, Credit Memo, Vendor Credit, Inventory Adjustment, 

## PRICING ##
class CostListHead(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=False, related_name='cost_list_head_item')
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, null=False, related_name='cost_list_head_vendor')
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    begin_effective_date = models.DateField(default=timezone.now, null=False)
    end_effective_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cost List for {self.item.item_name} - {self.vendor.vendor_name}"

class CostListLine(models.Model):
    cost_list_head = models.ForeignKey('CostListHead', on_delete=models.CASCADE, related_name='cost_lines')
    quantity = models.PositiveIntegerField(null=False, blank=False, help_text="Minimum quantity for this cost to apply")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    class Meta:
        unique_together = ('cost_list_head', 'quantity')
        ordering = ['quantity']

    def __str__(self):
        return f"{self.cost_list_head.item.item_name} - {self.quantity}+ units: ${self.cost}"
    
class PriceListHead(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=False, related_name='price_list_head_item')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=False, related_name='price_list_head_customer')
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    begin_effective_date = models.DateField(default=timezone.now, null=False)
    end_effective_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"price List for {self.item.item_name} - {self.customer.customer_name}"

class PriceListLine(models.Model):
    price_list_head = models.ForeignKey('PriceListHead', on_delete=models.CASCADE, related_name='price_lines')
    quantity = models.PositiveIntegerField(null=False, blank=False, help_text="Minimum quantity for this price to apply")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    class Meta:
        unique_together = ('price_list_head', 'quantity')
        ordering = ['quantity']

    def __str__(self):
        return f"{self.price_list_head.item.item_name} - {self.quantity}+ units: ${self.price}"    

## BLANKETS AND CONTRACTS ##
class ContractHead(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='contract_head_customer')
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    begin_effective_date = models.DateField(default=timezone.now, null=False, blank=False)
    end_effective_date = models.DateField(null=True, blank=True)
    reference_number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    
    def __str__(self):
        return f"Contract {self.reference_number} - {self.customer}"

class ContractLine(models.Model):
    contract = models.ForeignKey(ContractHead, on_delete=models.CASCADE, related_name='contract_items')
    item = models.ForeignKey('Item', on_delete=models.PROTECT)
    contract_quantity = models.PositiveIntegerField(null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    minimum_release_quantity = models.PositiveIntegerField(null=True, blank=True)
    purchased_quantity = models.PositiveIntegerField(default=0, null=False, blank=False)
    received_quantity = models.PositiveIntegerField(default=0, null=False, blank=False)
    sold_quantity = models.PositiveIntegerField(default=0, null=False, blank=False)
    
    def __str__(self):
        return f"Item {self.item} in Contract {self.contract.reference_number}"
    
## SALES ORDERS ##
class DropShipHead(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_customer')
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    bill_to_street = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_bill_to_street')
    bill_to_pobox = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_bill_to_pobox')
    bill_to_city = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_bill_to_city')
    bill_to_state = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_bill_to_state')
    bill_to_zip = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_bill_to_zip')
    ship_from_street = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_ship_from_street')
    ship_from_pobox = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_ship_from_pobox')
    ship_from_city = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_ship_from_city')
    ship_from_state = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_ship_from_state')
    ship_from_zip = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_ship_from_zip')
    ship_to_street = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_ship_to_street')
    ship_to_pobox = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_ship_to_pobox')
    ship_to_city = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_ship_to_city')
    ship_to_state = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_ship_to_state')
    ship_to_zip = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_ship_to_zip')
    customer_order_number = models.CharField(max_length=50, blank=True)
    terms = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_terms')
    requested_date = models.DateField()
    sales_rep = models.ForeignKey('SalesRep', on_delete=models.PROTECT, null=False, related_name='drop_ship_head_sales_rep')
    ms_po_number = models.ForeignKey('PurchaseHead', on_delete=models.SET_NULL, null=True, related_name='drop_ship_head_ms_po_number')
    vendor_due_date = models.ForeignKey('PurchaseHead', on_delete=models.SET_NULL, null=True, related_name='drop_ship_head_vendor_due_date')
    ship_from = models.ForeignKey('PurchaseHead', on_delete=models.PROTECT, null=True, related_name='drop_ship_head_ship_from')
    csr = models.ForeignKey('Employee', on_delete=models.PROTECT, null=True, related_name='drop_ship_head_csr')
    buyer = models.ForeignKey('PurchaseHead', on_delete=models.PROTECT, null=True, related_name='drop_ship_head_buyer')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f"Direct Order {self.number} for {self.customer}"
    
    @property
    def total_amount(self):
        return self.order_lines.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0

class DropShipLine(models.Model):
    dropship_head = models.ForeignKey('DropShipHead', on_delete=models.CASCADE, related_name='order_lines')
    item = models.ForeignKey('Item', on_delete=models.PROTECT, blank=False, null=False)
    contract = models.ForeignKey('ContractHead', on_delete=models.PROTECT, blank=True, null=True)
    quantity = models.PositiveIntegerField(null=False, blank=False) 
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)
    tax = models.ForeignKey('Tax', on_delete=models.PROTECT, null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True) 
    

    def __str__(self):
        return f"Item {self.item.item_name} in Drop Ship Order {self.dropship_order_head.number}"
        
class ReleaseHead(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='release_head_customer')
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    bill_to_street = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='release_head_bill_to_street')
    bill_to_pobox = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='release_head_bill_to_pobox')
    bill_to_city = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='release_head_bill_to_city')
    bill_to_state = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='release_head_bill_to_state')
    bill_to_zip = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='release_head_bill_to_zip')
    ship_to_street = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='release_head_ship_to_street')
    ship_to_pobox = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='release_head_ship_to_pobox')
    ship_to_city = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='release_head_ship_to_city')
    ship_to_state = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='release_head_ship_to_state')
    ship_to_zip = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='release_head_ship_to_zip')
    customer_order_number = models.CharField(max_length=50, blank=True)
    terms = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='release_head_terms')
    requested_date = models.DateField()
    ship_date = models.DateField()
    sales_rep = models.ForeignKey('SalesRep', on_delete=models.PROTECT, null=False, related_name='release_head_sales_rep')
    csr = models.ForeignKey('Employee', on_delete=models.PROTECT, null=True, related_name='release_head_csr')
    priority = models.PositiveIntegerField(default=0)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    class Meta:
        ordering = ['date_created', 'priority']
        
    def __str__(self):
        return f"Direct Order {self.number} for {self.customer}"
    
    @property
    def total_amount(self):
        return self.release_lines.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0
    
class ReleaseLine(models.Model):
    release_head = models.ForeignKey('ReleaseHead', on_delete=models.CASCADE, related_name='release_lines')
    item = models.ForeignKey('Item', on_delete=models.PROTECT, blank=False, null=False)
    quantity = models.PositiveIntegerField(null=False, blank=False) 
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)
    tax = models.ForeignKey('Tax', on_delete=models.PROTECT, null=True, blank=True, related_name='release_line_tax')
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True) 
    

    def __str__(self):
        return f"Item {self.item.item_name} in Release {self.release.number}"   


## PURCHASE ORDERS ## 
class PurchaseHead(models.Model):
    CATEGORY_TYPES =[
        ('d', 'Drop Ship'),
        ('w', 'Warehouse'),
        ('c', 'Crossdock'),
    ]
    
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    category = models.CharField(choices=CATEGORY_TYPES, max_length=30)
    bill_from_street = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=False, related_name='purchase_head_bill_from_street')
    bill_from_pobox = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=False, related_name='purchase_head_bill_from_pobox')
    bill_from_city = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=False, related_name='purchase_head_bill_from_city')
    bill_from_state = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=False, related_name='purchase_head_bill_from_state')
    bill_from_zip = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=False, related_name='purchase_head_bill_from_zip')
    ship_from = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=True, related_name='purchase_head_location_name')
    ship_from_street = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=False, related_name='purchase_head_ship_from_street')
    ship_from_pobox = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=False, related_name='purchase_head_ship_from_pobox')
    ship_from_city = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=False, related_name='purchase_head_ship_from_city')
    ship_from_state = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=False, related_name='purchase_head_ship_from_state')
    ship_from_zip = models.ForeignKey('VendorLocation', on_delete=models.PROTECT, null=False, related_name='purchase_head_ship_from_zip')
    ship_to_street = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='purchase_head_ship_to_street')
    ship_to_pobox = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='purchase_head_ship_to_pobox')
    ship_to_city = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='purchase_head_ship_to_city')
    ship_to_state = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='purchase_head_ship_to_state')
    ship_to_zip = models.ForeignKey('CustomerLocation', on_delete=models.PROTECT, null=False, related_name='purchase_head_ship_to_zip')
    terms = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=False, related_name='purchase_head_terms')
    requested_date = models.DateField()
    vendor_due_date = models.DateField()
    csr = models.ForeignKey('Employee', on_delete=models.PROTECT, null=True, related_name='purchase_head_csr')
    buyer = models.ForeignKey('PurchaseHead', on_delete=models.PROTECT, null=True, related_name='purchase_head_buyer')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f"Purchase Order {self.number}"
    
    @property
    def total_amount(self):
        return self.order_lines.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0

class PurchaseLine(models.Model):
    purchase_head = models.ForeignKey('PurchaseHead', on_delete=models.CASCADE, related_name='purchase_lines')
    item = models.ForeignKey('Item', on_delete=models.PROTECT, blank=False, null=False)
    contract = models.ForeignKey('ContractHead', on_delete=models.PROTECT, blank=True, null=True)
    quantity = models.PositiveIntegerField(null=False, blank=False) 
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)
    tax = models.ForeignKey('Tax', on_delete=models.PROTECT, null=True, blank=True, related_name='purchase_line_tax')
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True) 
    

    def __str__(self):
        return f"Item {self.item} in Purchase Order {self.purchase_head.number}"
        
# Inventory model