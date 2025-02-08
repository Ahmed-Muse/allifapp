from django.test import TestCase
from .models import CommonTaxParametersModel
from allifmaalusersapp.models import User
from django.urls import reverse
# Create your tests here.
class CommonTaxParametersModelTest(TestCase):

    def test_string_representation(self):
        creator=User.objects.create(username="Ahmed",email='ahmed@allifmaal.com')
        creator.save()
        item =CommonTaxParametersModel(taxname="Galmudugtax",taxdescription="description",owner=creator)
        item.save()
        record = CommonTaxParametersModel.objects.filter(id=1).first()
        self.assertEqual(record.owner.username, "Ahmed")        
        self.assertEqual(str(item), item.taxname,item.taxdescription)

        
        author = User.objects.get(id=1)
        field_label = author._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

        max_length = author._meta.get_field('username').max_length
        self.assertEqual(max_length, 255)

       
    def test_quantity(self):
        item =CommonTaxParametersModel(taxname="Puntlandtax",taxdescription="mydescription",taxrate=10.00)
        self.assertEqual(item.taxrate,10.00)
    def test_create_author_and_book(self):
        author = User.objects.create(username="Ahmed Muse")
        book = CommonTaxParametersModel.objects.create(taxname="Muse Diriye", owner=author)
        self.assertEqual(book.owner.username, "Ahmed Muse")

class BookTestCase(TestCase):
    def test_fields_author_name(self):
        author = User(username="Ahmed Muse")
        author.save()
        book =CommonTaxParametersModel(taxname="Tax Name", owner=author)
        book.save()

        # assertion example ...
        record = CommonTaxParametersModel.objects.get(id=1)
        self.assertEqual(record.owner.username, "Ahmed Muse")   

class ViewTest(TestCase):

    def test_commonwebsite_view(self):
        response = self.client.get(reverse('allifmaalcommonapp:commonWebsite'))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'allifmaalcommonapp/website/website.html')      




class BookDetailViewTest(TestCase):

    def setUp(self):
        self.owner= User.objects.create(username="Ahmed Muse")
        self.tax= CommonTaxParametersModel.objects.create(taxname="tax name", owner=self.owner)
"""
    def test_book_detail_view_success(self):
        url = reverse('allifmaalcommonapp:commonhrm', args=[self.owner.id, self.tax.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CommonTaxParametersModel: tax name")
        self.assertContains(response, "User: Ahmed Muse")

    def test_book_detail_view_author_not_found(self):
        url = reverse('allifmaalcommonapp:commonhrm', args=[999, self.tax.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Author not found")

    def test_book_detail_view_book_not_found(self):
        url = reverse('allifmaalcommonapp:commonhrm', args=[self.owner.id, 999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Book not found")
        """
