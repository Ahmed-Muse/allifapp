from django.test import TestCase, Client
from django.urls import reverse
from .models import CommonDivisionsModel

class NameIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        allifusr = 'allifmaal'
        allifslug = 'allifmaapengineering'
        
        # Generate the URL for the view with parameters
        self.url = reverse('allifmaalcommonapp:commonAddDivision',kwargs={'allifusr': allifusr, 'allifslug': allifslug})

    def test_name_list_integration(self):
        # Create test data
        CommonDivisionsModel.objects.create(division='ali', address='sadi road')
        CommonDivisionsModel.objects.create(division='omar', address='xamar')

        # Send a GET request to the URL
        response = self.client.get(self.url)

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Division')
        self.assertContains(response, 'allifmaal')
    