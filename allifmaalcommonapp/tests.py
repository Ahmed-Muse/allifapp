from django.test import TestCase
from .models import CommonTaxParametersModel

# Create your tests here.
class CommonTaxParametersModelTest(TestCase):

    def test_string_representation(self):
        item =CommonTaxParametersModel(taxname="Galmudugtax",taxdescription="description")
        self.assertEqual(str(item), item.taxname,item.taxdescription)
    
    def test_quantity(self):
        item =CommonTaxParametersModel(taxname="Puntlandtax",taxdescription="mydescription",taxrate=10.00)
        self.assertEqual(item.taxrate,10.00)
