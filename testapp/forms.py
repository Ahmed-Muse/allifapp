# apps/inventory/forms.py

from django import forms
from .models import TransferOrder, TransferOrderItem, Product, Location, GoodsIssueNote, GoodsReceiptNote
from .models import get_current_company # To get current company

class TransferOrderForm(forms.ModelForm):
    class Meta:
        model = TransferOrder
        fields = ['source_location', 'destination_location', 'order_date', 'expected_delivery_date', 'description']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        # Filter locations by the current company
        if self.company:
            self.fields['source_location'].queryset = Location.objects.filter(company=self.company)
            self.fields['destination_location'].queryset = Location.objects.filter(company=self.company)

    def clean(self):
        cleaned_data = super().clean()
        source_location = cleaned_data.get('source_location')
        destination_location = cleaned_data.get('destination_location')

        if source_location and destination_location and source_location == destination_location:
            raise forms.ValidationError("Source and Destination locations cannot be the same.")
        return cleaned_data

class TransferOrderItemForm(forms.ModelForm):
    class Meta:
        model = TransferOrderItem
        fields = ['product', 'quantity'] # transferred_unit_cost will be set by view logic

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if self.company:
            self.fields['product'].queryset = Product.objects.filter(company=self.company)

# Formset for Transfer Order Items
from django.forms import inlineformset_factory
TransferOrderItemFormSet = inlineformset_factory(
    TransferOrder,
    TransferOrderItem,
    form=TransferOrderItemForm,
    extra=1, # One empty form for adding
    can_delete=True,
    fields=['product', 'quantity']
)

class GoodsIssueNoteForm(forms.ModelForm):
    class Meta:
        model = GoodsIssueNote
        fields = ['issue_date', 'description']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GoodsReceiptNoteForm(forms.ModelForm):
    class Meta:
        model = GoodsReceiptNote
        fields = ['receipt_date', 'description']
        widgets = {
            'receipt_date': forms.DateInput(attrs={'type': 'date'}),
        }