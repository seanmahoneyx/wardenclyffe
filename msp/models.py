from django.db import models
from django.utils import timezone


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
    item_type = models.CharField(choices=ITEM_TYPES)
    revision = models.PositiveSmallIntegerField(blank=True, null=True)
    division = models.CharField(choices=DIVISION_TYPES)
    purch_desc = models.TextField(verbose_name="Purchase Description")
    sell_desc = models.TextField(verbose_name="Sell Description")
    category = models.CharField(choices=CATEGORY_TYPES, max_length=30)
    test = models.CharField(choices=CATEGORY_TYPES, max_length=10)
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
    cogs_acct = models.ForeignKey('Account',blank=False, on_delete=models.SET_NULL, null=True)
    asset_acct = models.ForeignKey('Account',blank=False, on_delete=models.SET_NULL, null=True)
    sale_acct = models.ForeignKey('Account',blank=False, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey('Customer',blank=False, on_delete=models.SET_NULL, null=True)
    is_taxable = models.BooleanField(default=False, blank=False, null=False)
    tax = models.ForeignKey('Tax',blank=True, on_delete=models.SET_NULL, null=True)
    
    
    def __str__(self):
        return self.item_name

class Salesrep(models.Model):
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
    is_active = models.BooleanField(default=True)
    account_type = models.CharField(max_length=50, blank=False)
    account_name = models.CharField(unique=True, max_length=100, blank=False)
    account_desc = models.TextField(blank=True)
    parent_account = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subaccounts')

    def __str__(self):
        return self.account_name

class Customer(models.Model):
    customer_name = models.CharField(unique=True, max_length=100, blank=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    is_active = models.BooleanField(default=True)
    bill_street = models.CharField(max_length=100, blank=False)
    bill_pobox = models.CharField(max_length=100, blank=False)
    bill_city = models.CharField(max_length=60, blank=False)
    bill_state = models.CharField(max_length=2, blank=False)
    bill_zip = models.PositiveIntegerField(blank=False)
    main_phone = models.CharField(max_length=15, blank=True)
    main_email = models.EmailField(max_length=254, blank=True)
    ap_email = models.EmailField(max_length=254, blank=True)
    fax = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)
    credit_limit = models.PositiveIntegerField()
    sales_rep = models.ForeignKey(Salesrep, on_delete=models.SET_NULL, null=True)
    csr = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    terms = models.ForeignKey(Terms, on_delete=models.SET_NULL, null=True)
    tax_code = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True)
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
    terms = models.ForeignKey(Terms, on_delete=models.SET_NULL, null=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return self.vendor_name

class Location(models.Model):
    is_active = models.BooleanField(default=True)    
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)   
    location_name = models.CharField(max_length=100, unique=True)
    street = models.CharField(max_length=100, blank=False)
    pobox = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=60, blank=False)
    state = models.CharField(max_length=2, blank=False)
    zip = models.PositiveIntegerField(blank=False)
    contact_name = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, related_name="name")
    contact_phone = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, related_name="phone")
    contact_email = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, related_name="email")
    delivery_open = models.TimeField()
    delivery_close = models.TimeField()
    is_boxtruck_able = models.BooleanField(default=True, null=False, blank=False)
    is_trailer_able = models.BooleanField(default=True, null=False, blank=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer} {self.ship_to_name}"


############ DYNAMIC MODELS ##################

#TODO
# Transaction models
# NONPOSTING- Sales Order, Purchase Order, Quote, Blanket, Contract 
# POSTING- Invoice, Bill, Item Receipt, Credit Memo, Vendor Credit, Inventory Adjustment, 

class ContractHead(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False)
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
    minimum_release_quantity = models.PositiveIntegerField(null=False, blank=False)
    purchased_quantity = models.PositiveIntegerField(default=0, null=False, blank=False)
    received_quantity = models.PositiveIntegerField(default=0, null=False, blank=False)
    sold_quantity = models.PositiveIntegerField(default=0, null=False, blank=False)
    
    def __str__(self):
        return f"Item {self.item} in Contract {self.contract.reference_number}"
    

class DropShipHead(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    bill_street = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='bill_street')
    bill_pobox = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='bill_pobox')
    bill_city = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='bill_city')
    bill_state = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='bill_state')
    bill_zip = models.ForeignKey('Customer', on_delete=models.PROTECT, null=False, related_name='bill_zip')
    ship_street = models.ForeignKey('Location', on_delete=models.PROTECT, null=False, related_name='street')
    ship_pobox = models.ForeignKey('Location', on_delete=models.PROTECT, null=False, related_name='pobox')
    ship_city = models.ForeignKey('Location', on_delete=models.PROTECT, null=False, related_name='city')
    ship_state = models.ForeignKey('Location', on_delete=models.PROTECT, null=False, related_name='state')
    ship_zip = models.ForeignKey('Location', on_delete=models.PROTECT, null=False, related_name='zip')
    customer_order_number = models.CharField(max_length=50, blank=True)
    terms = models.ForeignKey('Terms', on_delete=models.PROTECT, null=False)
    requested_date = models.DateField()
    sales_rep = models.ForeignKey('SalesRep', on_delete=models.PROTECT, null=False)
    ms_po_number = models.ForeignKey('PurchaseOrder', on_delete=models.SET_NULL, null=True, related_name='ms_po_number')
    vendor_due_date = models.ForeignKey('PurchaseOrder', on_delete=models.SET_NULL, null=True, related_name='vendor_due_date')
    ship_from = models.ForeignKey('PurchaseOrder', on_delete=models.PROTECT, null=True, related_name='ship_from')
    csr = models.ForeignKey('Employee', on_delete=models.PROTECT, null=True, related_name='csr')
    buyer = models.ForeignKey('PurchaseOrder', on_delete=models.PROTECT, null=True, related_name='buyer')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f"Direct Order {self.number} for {self.customer}"

class DropShipLine(models.Model):
    dropship_head = models.ForeignKey('DropShipHead', on_delete=models.CASCADE, related_name='order_lines')
    item = models.ForeignKey('Item', on_delete=models.PROTECT, blank=False, null=False)
    quantity = models.PositiveIntegerField(null=False, blank=False) 
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)
    tax = models.ForeignKey('Tax', on_delete=models.PROTECT, null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True) 
    

    def __str__(self):
        return f"Item {self.item.item_name} in Drop Ship Order {self.dropship_order_head.number}"
        
    
    

        
# Inventory model

# Vendor Price List (header + body)

# Customer Price List (header + body)