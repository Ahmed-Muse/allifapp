from django.shortcuts import render

# Create your views here.
def testinapp(request):

    context={

    }

    return render(request,'test.html',context)


# apps/inventory/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required # Assuming user authentication
from django.contrib import messages # For user feedback
import uuid # For generating unique numbers

from .models import get_current_company
#from apps.erp_accounting.models import ChartOfAccount, JournalEntry, JournalEntryLine, Transaction
from .models import *
from .forms import TransferOrderForm, TransferOrderItemFormSet, GoodsIssueNoteForm, GoodsReceiptNoteForm

# --- Helper Function for Accounting Entries (can be moved to a service layer) ---
def post_transfer_journal_entry(company, transaction_type, transfer_order, issued_or_received_by):
    """
    Generates the journal entry for GIN or GRN.
    transaction_type: 'GIN' or 'GRN'
    """
    try:
        with transaction.atomic():
            # Create a high-level ERP Transaction record
            erp_transaction = Transaction.objects.create(
                company=company,
                transaction_date=timezone.now().date(),
                description=f"Inventory Transfer {transaction_type} for TO {transfer_order.order_number}",
                reference_number=f"{transaction_type}-{transfer_order.order_number}",
            )

            journal_narration = ""
            debit_account = None
            credit_account = None

            # Get the "Inventory in Transit" account (assuming it exists in CoA)
            # You should ensure this account is set up for each company
            inventory_in_transit_account = ChartOfAccount.objects.get(
                company=company, account_number='11399' # Example account number
            )

            if transaction_type == 'GIN':
                journal_narration = f"Goods Issued from {transfer_order.source_location.name} for Transfer Order {transfer_order.order_number}"
                debit_account = inventory_in_transit_account # Inventory in Transit increases
                credit_account = transfer_order.source_location.inventory_asset_account # Source location inventory decreases
            elif transaction_type == 'GRN':
                journal_narration = f"Goods Received at {transfer_order.destination_location.name} for Transfer Order {transfer_order.order_number}"
                debit_account = transfer_order.destination_location.inventory_asset_account # Destination location inventory increases
                credit_account = inventory_in_transit_account # Inventory in Transit decreases
            else:
                raise ValueError("Invalid transaction_type for posting journal entry.")

            journal_entry = JournalEntry.objects.create(
                company=company,
                transaction=erp_transaction,
                entry_date=timezone.now().date(),
                narration=journal_narration,
            )

            total_transfer_value = sum(item.total_transferred_value() for item in transfer_order.items.all())

            JournalEntryLine.objects.create(
                journal_entry=journal_entry,
                account=debit_account,
                debit=total_transfer_value,
                credit=Decimal('0.00')
            )
            JournalEntryLine.objects.create(
                journal_entry=journal_entry,
                account=credit_account,
                debit=Decimal('0.00'),
                credit=total_transfer_value
            )

            if not journal_entry.is_balanced():
                raise Exception("Journal Entry is not balanced!")

            return journal_entry

    except ChartOfAccount.DoesNotExist:
        messages.error(issued_or_received_by, "Required accounting accounts (e.g., Inventory in Transit) are not configured in your Chart of Accounts.")
        raise
    except Exception as e:
        messages.error(issued_or_received_by, f"Error generating journal entry: {e}")
        raise


# --- Transfer Order Views ---

@login_required
def transfer_order_list(request):
    company = get_current_company()
    if not company:
        messages.error(request, "No active company selected.")
        return redirect('some_company_selection_page') # Redirect to a page where user selects/creates company

    transfer_orders = TransferOrder.objects.filter(company=company).order_by('-order_date')
    context = {
        'transfer_orders': transfer_orders,
        'current_company': company,
    }
    return render(request, 'inventory/transfer_order_list.html', context)

@login_required
def transfer_order_create(request):
    company = get_current_company()
    if not company:
        messages.error(request, "No active company selected.")
        return redirect('admin:index')

    if request.method == 'POST':
        form = TransferOrderForm(request.POST, company=company)
        formset = TransferOrderItemFormSet(request.POST, prefix='items', company=company)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                transfer_order = form.save(commit=False)
                transfer_order.company = company
                transfer_order.initiated_by = request.user
                transfer_order.order_number = f"TO-{uuid.uuid4().hex[:8].upper()}" # Auto-generate
                transfer_order.save()

                for item_form in formset:
                    if item_form.cleaned_data.get('DELETE'):
                        continue # Skip deleted forms in formset

                    item = item_form.save(commit=False)
                    item.company = company
                    item.transfer_order = transfer_order
                    
                    # Set transferred_unit_cost based on current inventory cost at source
                    source_inventory = Inventory.objects.filter(
                        company=company,
                        product=item.product,
                        location=transfer_order.source_location
                    ).first()
                    if not source_inventory or source_inventory.quantity < item.quantity:
                        messages.error(request, f"Insufficient stock for {item.product.name} at {transfer_order.source_location.name}.")
                        raise Exception("Insufficient stock") # Rollback transaction
                    
                    item.transferred_unit_cost = source_inventory.unit_cost
                    item.save()

                messages.success(request, "Transfer Order created successfully!")
                return redirect('transfer_order_detail', pk=transfer_order.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = TransferOrderForm(company=company)
        formset = TransferOrderItemFormSet(prefix='items', company=company)

    context = {
        'form': form,
        'formset': formset,
        'current_company': company,
    }
    return render(request, 'inventory/transfer_order_form.html', context)

@login_required
def transfer_order_detail(request, pk):
    company = get_current_company()
    transfer_order = get_object_or_404(TransferOrder, pk=pk, company=company)
    context = {
        'transfer_order': transfer_order,
        'current_company': company,
    }
    return render(request, 'inventory/transfer_order_detail.html', context)

@login_required
def transfer_order_approve(request, pk):
    company = get_current_company()
    transfer_order = get_object_or_404(TransferOrder, pk=pk, company=company)

    # Implement approval logic here (e.g., check user permissions)
    if not request.user.has_perm('inventory.can_approve_transfer_order'): # Custom permission
        messages.error(request, "You do not have permission to approve transfer orders.")
        return redirect('transfer_order_detail', pk=pk)

    if transfer_order.status == 'Draft' or transfer_order.status == 'Pending Approval':
        transfer_order.status = 'Approved'
        transfer_order.save()
        messages.success(request, f"Transfer Order {transfer_order.order_number} approved.")
    else:
        messages.warning(request, f"Transfer Order {transfer_order.order_number} cannot be approved from its current status.")
    return redirect('transfer_order_detail', pk=pk)

# --- GIN Views ---

@login_required
def create_gin(request, to_pk):
    company = get_current_company()
    transfer_order = get_object_or_404(TransferOrder, pk=to_pk, company=company)

    if transfer_order.status not in ['Approved', 'Issued']: # Can create GIN if approved or already issued (for re-issue)
        messages.error(request, "Transfer Order must be Approved to create a Goods Issue Note.")
        return redirect('transfer_order_detail', pk=to_pk)
    
    if hasattr(transfer_order, 'goods_issue_note') and transfer_order.goods_issue_note:
        messages.warning(request, "A GIN already exists for this Transfer Order. Editing existing GIN.")
        return redirect('gin_detail', pk=transfer_order.goods_issue_note.pk)

    if request.method == 'POST':
        form = GoodsIssueNoteForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                gin = form.save(commit=False)
                gin.company = company
                gin.transfer_order = transfer_order
                gin.issued_by = request.user
                gin.gin_number = f"GIN-{uuid.uuid4().hex[:8].upper()}" # Auto-generate

                # --- Inventory Deduction Logic ---
                for item in transfer_order.items.all():
                    source_inventory = Inventory.objects.get(
                        company=company,
                        product=item.product,
                        location=transfer_order.source_location
                    )
                    if source_inventory.quantity < item.quantity:
                        messages.error(request, f"Insufficient stock for {item.product.name} at {transfer_order.source_location.name}.")
                        raise Exception("Insufficient stock for GIN") # Rollback transaction
                    
                    source_inventory.quantity -= item.quantity
                    source_inventory.save()

                # --- Post Journal Entry for GIN ---
                try:
                    gin_je = post_transfer_journal_entry(company, 'GIN', transfer_order, request.user)
                    gin.journal_entry = gin_je
                except Exception as e:
                    messages.error(request, f"Failed to post GIN accounting entry: {e}")
                    raise # Re-raise to rollback transaction

                gin.save() # Save the GIN record
                
                transfer_order.status = 'Issued' # Update TO status
                transfer_order.save()

                messages.success(request, f"Goods Issue Note {gin.gin_number} created and posted successfully.")
                return redirect('gin_detail', pk=gin.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = GoodsIssueNoteForm()

    context = {
        'form': form,
        'transfer_order': transfer_order,
        'current_company': company,
    }
    return render(request, 'inventory/gin_form.html', context)

@login_required
def gin_detail(request, pk):
    company = get_current_company()
    gin = get_object_or_404(GoodsIssueNote, pk=pk, company=company)
    context = {
        'gin': gin,
        'transfer_order': gin.transfer_order,
        'current_company': company,
    }
    return render(request, 'inventory/gin_detail.html', context)

# --- GRN Views ---save() can_approve_transfer_order

@login_required
def create_grn(request, to_pk):
    company = get_current_company()
    transfer_order = get_object_or_404(TransferOrder, pk=to_pk, company=company)

    if transfer_order.status != 'Issued':
        messages.error(request, "Transfer Order must be Issued to create a Goods Receipt Note.")
        return redirect('transfer_order_detail', pk=to_pk)

    if hasattr(transfer_order, 'goods_receipt_note') and transfer_order.goods_receipt_note:
        messages.warning(request, "A GRN already exists for this Transfer Order. Editing existing GRN.")
        return redirect('grn_detail', pk=transfer_order.goods_receipt_note.pk)

    if request.method == 'POST':
        form = GoodsReceiptNoteForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                grn = form.save(commit=False)
                grn.company = company
                grn.transfer_order = transfer_order
                grn.received_by = request.user
                grn.grn_number = f"GRN-{uuid.uuid4().hex[:8].upper()}" # Auto-generate

                # --- Inventory Addition Logic ---
                for item in transfer_order.items.all():
                    destination_inventory, created = Inventory.objects.get_or_create(
                        company=company,
                        product=item.product,
                        location=transfer_order.destination_location,
                        defaults={'quantity': Decimal('0.00'), 'unit_cost': Decimal('0.00')}
                    )
                    
                    # Weighted Average Costing Update (if item already exists at destination)
                    if not created and destination_inventory.quantity > Decimal('0.00'):
                        old_total_value = destination_inventory.quantity * destination_inventory.unit_cost
                        new_total_value = old_total_value + (item.quantity * item.transferred_unit_cost)
                        new_total_quantity = destination_inventory.quantity + item.quantity
                        destination_inventory.unit_cost = new_total_value / new_total_quantity
                    else: # First time product at this location, or quantity was zero
                        destination_inventory.unit_cost = item.transferred_unit_cost

                    destination_inventory.quantity += item.quantity
                    destination_inventory.save()

                # --- Post Journal Entry for GRN ---
                try:
                    grn_je = post_transfer_journal_entry(company, 'GRN', transfer_order, request.user)
                    grn.journal_entry = grn_je
                except Exception as e:
                    messages.error(request, f"Failed to post GRN accounting entry: {e}")
                    raise # Re-raise to rollback transaction

                grn.save() # Save the GRN record

                transfer_order.status = 'Received' # Update TO status
                transfer_order.save()

                messages.success(request, f"Goods Receipt Note {grn.grn_number} created and posted successfully.")
                return redirect('grn_detail', pk=grn.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = GoodsReceiptNoteForm()

    context = {
        'form': form,
        'transfer_order': transfer_order,
        'current_company': company,
    }
    return render(request, 'inventory/grn_form.html', context)

@login_required
def grn_detail(request, pk):
    company = get_current_company()
    grn = get_object_or_404(GoodsReceiptNote, pk=pk, company=company)
    context = {
        'grn': grn,
        'transfer_order': grn.transfer_order,
        'current_company': company,
    }
    return render(request, 'inventory/grn_detail.html', context)