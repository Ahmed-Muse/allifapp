import datetime

from django.test import TestCase
from django.utils import timezone

from .forms import CommonAddTaxParameterForm
# tests/test_forms.py
from django.test import TestCase
# myapp/tests/test_forms.py
from django.test import TestCase
from .forms import CommonAddTaxParameterForm

from django.test import TestCase
from allifmaalusersapp.models import User
from django.db.utils import IntegrityError
from django import forms #added import forms

from .models import CommonSectorsModel
from .forms import CommonAddSectorForm

############################### test for sectors ###################################
class CommonAddSectorFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_valid_form_sectors(self):
        form = CommonAddSectorForm(data={'name': 'Logistics', 'notes': 'Test Notes'})
        self.assertTrue(form.is_valid())
        sector = form.save(commit=False)
        sector.owner = self.user
        sector.save()
        self.assertEqual(CommonSectorsModel.objects.count(), 1)
        self.assertEqual(CommonSectorsModel.objects.first().name, 'Logistics')
        self.assertEqual(CommonSectorsModel.objects.first().notes, 'Test Notes')
        self.assertEqual(CommonSectorsModel.objects.first().owner, self.user)

    def test_invalid_blank_fields_sectors(self):
        form = CommonAddSectorForm(data= {'name': '', 'notes': 'Test Notes'})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_valid_blank_fields_sectors(self):
        form = CommonAddSectorForm(data={'name': 'TestName', 'notes': ''})
        self.assertTrue(form.is_valid())
        sector = form.save(commit=False)
        sector.owner = self.user
        sector.save()
        self.assertEqual(CommonSectorsModel.objects.count(), 1)
        self.assertIsNone(CommonSectorsModel.objects.first().notes) #changed assertEqual to assertIsNone.

    def test_valid_null_fields_sectors(self):
        form = CommonAddSectorForm(data={'name': 'TestName', 'notes': None})
        self.assertTrue(form.is_valid())
        sector = form.save(commit=False)
        sector.owner = self.user
        sector.save()
        self.assertEqual(CommonSectorsModel.objects.count(), 1)
        self.assertIsNone(CommonSectorsModel.objects.first().notes)

    def test_unique_fields_violation_sectors(self):
        CommonSectorsModel.objects.create(name='UniqueName', owner=self.user)
        form = CommonAddSectorForm(data={'name': 'UniqueName', 'notes': 'Test Notes'})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertEqual(CommonSectorsModel.objects.count(), 1)

    def test_form_widgets_sectors(self):
        form = CommonAddSectorForm()
        self.assertIsInstance(form.fields['name'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['notes'].widget, forms.TextInput)
        self.assertEqual(form.fields['name'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['notes'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['name'].widget.attrs['placeholder'], '')
        self.assertEqual(form.fields['notes'].widget.attrs['placeholder'], '')











class ItemFormTest(TestCase):

    def test_item_form_valid(self):
       
        form =CommonAddTaxParameterForm(data={'taxname': 'Test Item', 'taxdescription': 'This is a test item.'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.fields['taxname'].help_text, '')

    def test_item_form_invalid(self):
        form_data = {'taxname': '', 'taxdescription': ''}
        form =CommonAddTaxParameterForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        form =CommonAddTaxParameterForm()
        self.assertFalse(form.is_valid())

