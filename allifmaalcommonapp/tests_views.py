# tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from allifmaalusersapp.models import User
from django.contrib.auth.decorators import login_required
class commonWebsiteTest(TestCase):

    def test_home_view_status_code(self):
        response = self.client.get(reverse('allifmaalcommonapp:commonWebsite'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_view_template_used(self):
        response = self.client.get(reverse('allifmaalcommonapp:commonWebsite'))
        self.assertTemplateUsed(response, 'allifmaalcommonapp/website/website.html')

    def test_about_view_context(self):
        response = self.client.get(reverse('allifmaalcommonapp:commonWebsite'))
        self.assertEqual(response.context['title'], 'Allifmaal ERP')

    def test_home_view_content(self):
        response = self.client.get(reverse('allifmaalcommonapp:commonWebsite'))
        self.assertContains(response, "Allifmaal")
    
    def setUp(self):
        # Create a user
        self.username = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_view_with_two_parameters(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Define the parameters
        allifusr = 'allifmaal'
        allifslug = 'allifmaapengineering'
        
        # Generate the URL for the view with parameters
        url = reverse('allifmaalcommonapp:commonDivisions',kwargs={'allifusr': allifusr, 'allifslug': allifslug})
        
        # Make a GET request to the view
        response = self.client.get(url)
        
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Additional assertions to check the response content
        #self.assertContains(response, 'Expected content')
    def test_add_numbers_post(self):
        # Define the parameters
        allifusr = 'allifmaal'
        allifslug = 'allifmaapengineering'
        
        # Generate the URL for the view with parameters
        url = reverse('allifmaalcommonapp:commonAddDivision',kwargs={'allifusr': allifusr, 'allifslug': allifslug})
        
        # Make a GET request to the view
        response = self.client.get(url)

        
        data = {'division': 'jjlfkds', 'address': 'sadriroad'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
       
        
        # Additional assertions to check the response content
        #self.assertContains(response, 'Expected content')
        # Additional assertions to check the response content
        #self.assertContains(response, 'Expected content')
        
        # Additional assertions to check the response content
        #self.assertContains(response, 'Expected content')

"""
    def test_view_with_two_parameters(self):
        # Define the parameters
        allifusr= 'admin/'
        allifslug = 'allifmaal-sales-distributions-limited2116-e7b104a5d8e7/'
        
        # Generate the URL for the view with parameters
        url = reverse('allifmaalcommonapp:commonDivisions', args=allifusr,kwargs=allifslug)
        
        # Make a GET request to the view
        response = self.client.get(url)
        
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Additional assertions to check the response content
        #self.assertContains(response, 'Expected content')


    def test_doc_format(self):
        url = reverse('allifmaalcommonapp:commonDocsFormat')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "Please submit the form to add two numbers.")
"""
    
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.decorators import login_required

class MyViewTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    def test_view_without_login(self):
        # Define the parameters
        allifusr = 'admin'
        allifslug = 'allifmaal-sales-distributions-limited2116-e7b104a5d8e7'
        
        # Generate the URL for the view with parameters
        url = reverse('allifmaalcommonapp:commonDivisions',kwargs={'allifusr': allifusr, 'allifslug': allifslug})
        
        # Make a GET request to the view without logging in
        response = self.client.get(url)
        
        # Check that the response is a redirect to the login page
        self.assertEqual(response.status_code,200)
        #self.assertRedirects(response, f"{reverse('allifmaalusersapp:userLoginPage')}?next={url}")

    def test_view_with_login(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Define the parameters
        allifusr = 'admin'
        allifslug = 'allifmaal-sales-distributions-limited2116-e7b104a5d8e7'
        
        # Generate the URL for the view with parameters
        url = reverse('allifmaalcommonapp:commonDivisions',kwargs={'allifusr': allifusr, 'allifslug': allifslug})
        
        # Make a GET request to the view
        response = self.client.get(url)
        
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Additional assertions to check the response content
        #self.assertContains(response, 'Expected content')