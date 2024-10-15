from django.db import models


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
    
    # MODEL FIELDS
    item_name = models.CharField(unique=True, max_length=100)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    active_status = models.BooleanField(default=True)
    revision = models.PositiveSmallIntegerField(blank=True, null=True)
    division = models.CharField(choices=DIVISION_TYPES)
    purch_desc = models.TextField(verbose_name="Purchase Description")
    sell_desc = models.TextField(verbose_name="Sell Description")
    category = models.CharField(choices=CATEGORY_TYPES, max_length=30)
    test = models.CharField(choices=CATEGORY_TYPES, max_length=10)
    flute = models.CharField(max_length=6)
    paper = models.CharField(max_length=4)
    printed = models.BooleanField(default=False)
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
    
    def __str__(self):
        return self.item_name

class Salesrep(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Employee(models.Model):
    
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Terms(models.Model):
    name = models.CharField(unique=True, max_length=100, blank=False)
    net_due = models.PositiveSmallIntegerField()
    discount_percent = models.PositiveSmallIntegerField()  # Add validators if needed
    discount_days = models.PositiveSmallIntegerField()
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Tax(models.Model):
    code = models.CharField(unique=True, max_length=20, blank=False)
    tax_percent = models.PositiveSmallIntegerField()  # Add validators if needed
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Account(models.Model):
    active_status = models.BooleanField(default=True)
    account_type = models.CharField(max_length=50, blank=False)
    account_name = models.CharField(unique=True, max_length=100, blank=False)
    account_desc = models.TextField(blank=True)  # Optional description
    parent_account = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subaccounts')

    def __str__(self):
        return self.account_name

class Customer(models.Model):
    customer_name = models.CharField(unique=True, max_length=100, blank=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    active_status = models.BooleanField(default=True)
    bill_street = models.CharField(max_length=100, blank=True)
    bill_pobox = models.CharField(max_length=100, blank=True)
    bill_city = models.CharField(max_length=60, blank=True)
    bill_state = models.CharField(max_length=2, blank=True)
    bill_zip = models.PositiveIntegerField(blank=True)
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

    def __str__(self):
        return self.customer_name

class Vendor(models.Model):
    vendor_name = models.CharField(unique=True, max_length=100, blank=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    active_status = models.BooleanField(default=True)
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
    vend_1099 = models.BooleanField(default=True)
    terms = models.ForeignKey(Terms, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.vendor_name


### DYNAMIC MODELS ###

#TODO
# 1. Transaction model
# 2. Inventory model
