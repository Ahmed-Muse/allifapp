import datetime

from django.test import TestCase
from django.utils import timezone

from .forms import CommonAddTaxParameterForm
# tests/test_forms.py
from django.test import TestCase
# myapp/tests/test_forms.py
from django.test import TestCase
from .forms import CommonAddTaxParameterForm

class ItemFormTest(TestCase):

    def test_item_form_valid(self):
        form_data = {'taxname': 'Test Item', 'taxdescription': 'This is a test item.'}
        form =CommonAddTaxParameterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_item_form_invalid(self):
        form_data = {'taxname': '', 'taxdescription': ''}
        form =CommonAddTaxParameterForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)


"""
class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form =CommonAddTaxParameterForm()
        self.assertTrue(form.fields['taxname'].label is None or form.fields['taxname'].label == 'taxname')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
"""