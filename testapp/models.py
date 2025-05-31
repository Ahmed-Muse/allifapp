from django.db import models

# Create your models here.
# apps/core/models.py

from django.db import models
from django.conf import settings
from threading import local # <--- This is the import for 'local' from 'threading'

# Thread-local for current company
_thread_locals = local() # <--- 'local()' is used here to create a thread-local storage

def get_current_company():
    """
    Retrieves the current company from the thread-local storage.
    This allows accessing the company context from anywhere within the request processing thread.
    """
    return getattr(_thread_locals, 'company', None)

def set_current_company(company):
    """
    Sets the current company in the thread-local storage.
    This is typically called by the TenantMiddleware.
    """
    _thread_locals.company = company

# ... rest of your Company and BaseModel definitions ...

from django.db import models
from django.conf import settings
from threading import local

# Thread-local for current company
_thread_locals = local()

def get_current_company():
    return getattr(_thread_locals, 'company', None)

def set_current_company(company):
    _thread_locals.company = company

class Company(models.Model):
    """
    Represents a single tenant (e.g., a company subscribing to your ERP).
    Each company will have its own isolated data.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, help_text="Unique identifier for URL or identification")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CompanyScopedManager(models.Manager):
    """
    Custom manager to automatically filter queries by the current company.
    """
    def get_queryset(self):
        company = get_current_company()
        if company:
            return super().get_queryset().filter(company=company)
        # In a production multi-tenant app, you might raise an error here
        # or return an empty queryset if no company context is available
        return super().get_queryset()

class BaseModel(models.Model):
    """
    Abstract base model for all tenant-specific models.
    Automatically links to a Company and uses the CompanyScopedManager.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='%(class)ss')
    
    objects = CompanyScopedManager() # Custom manager for tenant-scoped queries
    all_objects = models.Manager()   # Default manager to access all objects (e.g., for admin)

    class Meta:
        abstract = True
        # Ensure that models inheriting from BaseModel have unique_together constraints
        # that include 'company' if they have unique fields.

# apps/core/models.py

from django.db import models
from django.conf import settings
from threading import local

# Thread-local for current company
_thread_locals = local()

def get_current_company():
    return getattr(_thread_locals, 'company', None)

def set_current_company(company):
    _thread_locals.company = company

class Company(models.Model):
    """
    Represents a single tenant (e.g., a company subscribing to your ERP).
    Each company will have its own isolated data.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, help_text="Unique identifier for URL or identification")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CompanyScopedManager(models.Manager):
    """
    Custom manager to automatically filter queries by the current company.
    """
    def get_queryset(self):
        company = get_current_company()
        if company:
            return super().get_queryset().filter(company=company)
        return super().get_queryset()

class BaseModel(models.Model):
    """
    Abstract base model for all tenant-specific models.
    Automatically links to a Company and uses the CompanyScopedManager.
    Includes common timestamps.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='%(class)ss')
    
    # --- ADD THESE TWO FIELDS ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # --------------------------
    
    objects = CompanyScopedManager() # Custom manager for tenant-scoped queries
    all_objects = models.Manager()   # Default manager to access all objects (e.g., for admin)

    class Meta:
        abstract = True
        # Ensure that models inheriting from BaseModel have unique_together constraints
        # that include 'company' if they have unique fields.
from django.db import models
from django.utils import timezone
from decimal import Decimal
#from apps.core.models import BaseModel # Inherit from BaseModel for multi-tenancy

# Assuming AccountType is defined elsewhere or directly within ChartOfAccount choices
# class AccountType(models.Model): ...

class ChartOfAccount(BaseModel):
    account_type_choices = [
        ('Asset', 'Asset'), ('Liability', 'Liability'), ('Equity', 'Equity'),
        ('Revenue', 'Revenue'), ('Expense', 'Expense')
    ]
    account_type = models.CharField(max_length=50, choices=account_type_choices)
    account_number = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent_account = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_accounts')
    is_active = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        unique_together = ('company', 'account_number')
        ordering = ['account_number']

    def __str__(self):
        return f"{self.account_number} - {self.name}"

class Transaction(BaseModel):
    transaction_date = models.DateField(default=timezone.now)
    description = models.TextField()
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, default='Posted') # e.g., Draft, Posted, Reversed

    class Meta(BaseModel.Meta):
        ordering = ['-transaction_date']

    def __str__(self):
        return f"Transaction {self.id} on {self.transaction_date}"

class JournalEntry(BaseModel):
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='journal_entry')
    entry_date = models.DateField(default=timezone.now)
    narration = models.TextField()
    status = models.CharField(max_length=50, default='Balanced') # For validation

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Journal Entries"
        ordering = ['-entry_date', '-created_at'] # Inherits created_at from BaseModel

    def __str__(self):
        return f"JE {self.id} - {self.narration[:50]}..."

    def is_balanced(self):
        # This relies on related_name='lines' in JournalEntryLine
        total_debits = sum(line.debit for line in self.lines.all())
        total_credits = sum(line.credit for line in self.lines.all())
        return total_debits == total_credits

class JournalEntryLine(BaseModel):
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(ChartOfAccount, on_delete=models.PROTECT, related_name='journal_entry_lines')
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    class Meta(BaseModel.Meta):
        # Custom validation to ensure debit XOR credit
        constraints = [
            models.CheckConstraint(
                check=models.Q(debit__gt=0, credit=0) | models.Q(debit=0, credit__gt=0),
                name='debit_xor_credit'
            )
        ]

    def __str__(self):
        return f"{self.account.name}: Debit {self.debit} / Credit {self.credit}"


# apps/inventory/models.py

from django.db import models
from django.utils import timezone
from decimal import Decimal
#from apps.core.models import BaseModel # For multi-tenancy
#from apps.erp_accounting.models import ChartOfAccount, JournalEntry, Transaction # For accounting integration
from django.conf import settings # For accessing AUTH_USER_MODEL

# 1. Product (Your CommonStocksModel equivalent)
class Product(BaseModel):
    """
    Defines a unique product/stock item.
    """
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100) # Stock Keeping Unit
    description = models.TextField(blank=True, null=True)
    # Default accounts for this product type (can be overridden by specific inventory entries)
    inventory_account = models.ForeignKey(ChartOfAccount, on_delete=models.PROTECT, related_name='product_inventory_items')
    cogs_account = models.ForeignKey(ChartOfAccount, on_delete=models.PROTECT, related_name='product_cogs_items')
    sales_account = models.ForeignKey(ChartOfAccount, on_delete=models.PROTECT, related_name='product_sales_items')
    
    # You might have a default unit cost here, but actual cost is tracked per Inventory entry
    # unit_cost = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))

    class Meta(BaseModel.Meta):
        unique_together = ('company', 'sku') # SKU must be unique per company

    def __str__(self):
        return f"{self.name} ({self.sku})"

# 2. Location (Represents a Branch/Warehouse/Store within a Company)
class Location(BaseModel):
    """
    Represents a physical location (e.g., branch, warehouse) where inventory is stored.
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, help_text="Unique code for the location")
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Each location should have its own specific Inventory Asset account in the CoA
    # This is crucial for tracking inventory value per branch on the Balance Sheet.
    inventory_asset_account = models.ForeignKey(
        ChartOfAccount,
        on_delete=models.PROTECT,
        related_name='location_inventory_assets',
        help_text="The Chart of Account for inventory held at this location (e.g., 11301 Inventory - Main Warehouse)"
    )

    class Meta(BaseModel.Meta):
        unique_together = ('company', 'code')

    def __str__(self):
        return f"{self.name} ({self.code})"

# 3. Inventory (Actual stock quantity and value at a specific location)
class Inventory(BaseModel):
    """
    Tracks the quantity and average cost of a Product at a specific Location.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_records')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='stock_at_location')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    # Weighted average cost for this product at this location
    unit_cost = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal('0.00')) 

    class Meta(BaseModel.Meta):
        unique_together = ('company', 'product', 'location')
        verbose_name_plural = "Inventories"

    def __str__(self):
        return f"{self.product.name} ({self.quantity} @ {self.unit_cost}) at {self.location.name}"

    @property
    def total_value(self):
        return self.quantity * self.unit_cost

# 4. Transfer Order (TO)
class TransferOrder(BaseModel):
    """
    A request to move stock between two locations within the same company.
    """
    order_number = models.CharField(max_length=100, unique=True) # Unique per company
    source_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='outgoing_transfer_orders')
    destination_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='incoming_transfer_orders')
    
    order_date = models.DateField(default=timezone.now)
    expected_delivery_date = models.DateField(null=True, blank=True)
    
    status_choices = [
        ('Draft', 'Draft'),
        ('Pending Approval', 'Pending Approval'), # For approval workflow
        ('Approved', 'Approved'), # Approved for issue
        ('Issued', 'Issued (GIN Created)'),
        ('Received', 'Received (GRN Created)'),
        ('Cancelled', 'Cancelled')
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='Draft')
    
    description = models.TextField(blank=True, null=True)
    initiated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='initiated_transfer_orders')

    class Meta(BaseModel.Meta):
        unique_together = ('company', 'order_number')
        ordering = ['-order_date', '-created_at'] # Inherits created_at

    def __str__(self):
        return f"TO {self.order_number} from {self.source_location.code} to {self.destination_location.code}"

# 5. Transfer Order Item (TOI)
class TransferOrderItem(BaseModel):
    """
    Individual line items on a Transfer Order.
    """
    transfer_order = models.ForeignKey(TransferOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    
    # The cost at which the item is being transferred (its cost at the source location)
    transferred_unit_cost = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal('0.00')) 

    class Meta(BaseModel.Meta):
        unique_together = ('company', 'transfer_order', 'product') # One product per TO

    def __str__(self):
        return f"{self.product.name} ({self.quantity} units) for TO {self.transfer_order.order_number}"

# 6. Goods Issue Note (GIN) - Created by the sending location
class GoodsIssueNote(BaseModel):
    """
    Document confirming the issue of goods from a source location for transfer.
    """
    transfer_order = models.OneToOneField(TransferOrder, on_delete=models.PROTECT, related_name='goods_issue_note')
    gin_number = models.CharField(max_length=100, unique=True) # Unique per company
    issue_date = models.DateField(default=timezone.now)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='gins_issued')
    description = models.TextField(blank=True, null=True)
    
    # Link to the generated JournalEntry for audit trail
    journal_entry = models.OneToOneField(JournalEntry, on_delete=models.SET_NULL, null=True, blank=True, related_name='gin')

    class Meta(BaseModel.Meta):
        unique_together = ('company', 'gin_number')
        ordering = ['-issue_date', '-created_at']

    def __str__(self):
        return f"GIN {self.gin_number} for TO {self.transfer_order.order_number}"

# 7. Goods Receipt Note (GRN) - Created by the receiving location
class GoodsReceiptNote(BaseModel):
    """
    Document confirming the receipt of goods at a destination location from transfer.
    """
    transfer_order = models.OneToOneField(TransferOrder, on_delete=models.PROTECT, related_name='goods_receipt_note')
    grn_number = models.CharField(max_length=100, unique=True) # Unique per company
    receipt_date = models.DateField(default=timezone.now)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='grns_received')
    description = models.TextField(blank=True, null=True)
    
    # Link to the generated JournalEntry for audit trail
    journal_entry = models.OneToOneField(JournalEntry, on_delete=models.SET_NULL, null=True, blank=True, related_name='grn')

    class Meta(BaseModel.Meta):
        unique_together = ('company', 'grn_number')
        ordering = ['-receipt_date', '-created_at']

    def __str__(self):
        return f"GRN {self.grn_number} for TO {self.transfer_order.order_number}"

# Optional: Inventory in Transit Account (for tracking goods during transfer)
# This account would be a ChartOfAccount entry (e.g., 11399 Inventory in Transit)
# You'd need to ensure this account exists in the company's CoA.