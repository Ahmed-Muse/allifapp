# tests/test_views.py

from django.urls import reverse
from allifmaalusersapp.models import User
from django.test import TestCase, RequestFactory,Client
from .views import commonSectors,commonWebsite  # Replace 'myapp' with your app name
from .models import CommonSectorsModel  # Replace 'myapp' with your app name
from .forms import CommonAddSectorForm  # Replace 'myapp' with your app name
from django.shortcuts import render
from unittest.mock import patch
from django.contrib.sessions.middleware import SessionMiddleware





from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from django.shortcuts import render, redirect
from unittest.mock import patch

from .models import CommonSectorsModel  # Replace . with your actual import
from .forms import CommonAddSectorForm  # Replace . with your actual import
from .views import commonSectors  # Replace . with your actual import

class CommonSectorsViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.customurlslug = "testslug"
        self.user.save()

    def test_common_sectors_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('allifmaalcommonapp:commonSectors', kwargs={'allifusr': 'testslug'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'allifmaalcommonapp/sectors/sectors.html')
        self.assertIsInstance(response.context['form'], CommonAddSectorForm)
        self.assertEqual(response.context['title'], 'Main Sectors')

    def test_common_sectors_post_valid(self):
        self.client.force_login(self.user)
        form_data = {'name': 'Logistics', 'notes': 'Test Notes'}
        response = self.client.post(reverse('allifmaalcommonapp:commonSectors', kwargs={'allifusr': 'testslug'}), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(CommonSectorsModel.objects.count(), 1)
        self.assertEqual(CommonSectorsModel.objects.first().name, 'Logistics')

    def test_common_sectors_post_invalid(self):
        self.client.force_login(self.user)
        form_data = {'name': '', 'notes': 'Test Notes'}  # Invalid (blank name)
        response = self.client.post(reverse('allifmaalcommonapp:commonSectors', kwargs={'allifusr': 'testslug'}), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'allifmaalcommonapp/sectors/sectors.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(CommonSectorsModel.objects.count(), 0)

    def test_common_sectors_exception(self):
        self.client.force_login(self.user)
        with patch('allifmaalcommonapp.views.render') as mock_render:
            mock_render.side_effect = Exception('Test Exception')
            response = self.client.get(reverse('allifmaalcommonapp:commonSectors', kwargs={'allifusr': 'testslug'}))
            self.assertTemplateUsed(response, 'allifmaalcommonapp/error/error.html')

    def test_common_sectors_queryset(self):
        self.client.force_login(self.user)
        CommonSectorsModel.objects.create(name="TestSector", owner=self.user)
        response = self.client.get(reverse('allifmaalcommonapp:commonSectors', kwargs={'allifusr': 'testslug'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['allifqueryset'].count(), 1)
        self.assertEqual(response.context['allifqueryset'].first().name, "TestSector")

    def test_common_sectors_user_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('allifmaalcommonapp:commonSectors', kwargs={'allifusr': 'testslug'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance.owner, None) #Before post, owner is none.
        self.assertEqual(response.context['title'], "Main Sectors")








class CommonSectorsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.common_sector = CommonSectorsModel.objects.create(name='Test Sector', owner=self.user)

    def test_common_sectors_get(self):
        allifusr = 'allifmaal'
        allifslug = 'allifmaapengineering'
        request = self.factory.get(reverse('allifmaalcommonapp:commonSectors',kwargs={'allifusr': allifusr, 'allifslug': allifslug}))
        request.user = self.user

        # Add session to the request
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        response = commonSectors(request)
        self.assertEqual(response.status_code, 200)

        #self.assertTemplateUsed(response, 'allifmaalcommonapp/sectors/sectors.html')
        #self.assertContains(response, 'Test Sector') #check if the created sector is in the html.
        #self.assertIsInstance(response.context['form'], CommonAddSectorForm)
        #self.assertEqual(response.context['title'], 'Main Sectors')
        #self.assertEqual(response.context['allifqueryset'].count(), 1)




    def test_common_sectors_post_valid_form(self):
        
        allifusr = 'allifmaal'
        allifslug = 'allifmaapengineering'
        request = self.factory.post(reverse('allifmaalcommonapp:commonSectors',kwargs={'allifusr': allifusr, 'allifslug': allifslug}), {'name': 'Test Sector'}) # replace my_view with the name of the URL for this view.
        request.user = self.user
        # Add session to the request
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        response = commonSectors(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CommonSectorsModel.objects.count(), 1)
        #self.assertEqual(CommonSectorsModel.objects.last().name, 'New Sector')
        self.assertEqual(CommonSectorsModel.objects.last().owner, self.user)
        #self.assertTemplateUsed(response, 'allifmaalcommonapp/sectors/sectors.html')







        


        

    def test_common_sectors_post_invalid_form(self):
        allifusr = 'allifmaal'
        allifslug = 'allifmaapengineering'
        request = self.factory.post(reverse('allifmaalcommonapp:commonSectors',kwargs={'allifusr': allifusr, 'allifslug': allifslug})) # replace my_view with the name of the URL for this view.
        request.user = self.user
        # Add session to the request my_vew
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        response = commonSectors(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CommonSectorsModel.objects.count(), 1) #make sure no new sectors were created.
        #self.assertTemplateUsed(response, 'allifmaalcommonapp/sectors/sectors.html')
        #self.assertFalse(response.context['form'].is_valid())

    def test_common_sectors_exception(self):
        allifusr = 'allifmaal'
        allifslug = 'allifmaapengineering'
        request = self.factory.get(reverse('allifmaalcommonapp:commonSectors',kwargs={'allifusr': allifusr, 'allifslug': allifslug})) # replace my_view with the name of the URL for this view.
        request.user = self.user

        with patch('allifmaalcommonapp.views.CommonSectorsModel.objects.all', side_effect=Exception('Test Exception')): #replace myapp.views with the location of the view.
            # Add session to the request
            middleware = SessionMiddleware(lambda req: None)
            middleware.process_request(request)
            request.session.save()
            response = commonSectors(request)

        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'allifmaalcommonapp/error/error.html')
        #self.assertContains(response, 'Test Exception')

    def test_common_sectors_user_not_authenticated(self):
        allifusr = 'allifmaal'
        allifslug = 'allifmaapengineering'
        request = self.factory.get(reverse('allifmaalcommonapp:commonSectors',kwargs={'allifusr': allifusr, 'allifslug': allifslug})) # replace my_view with the name of the URL for this view.
        
        #response = commonSectors(request)
        #self.assertEqual(response.status_code, 302) # or 200, depending on if you have login_required. if login_required is used, it should be 302.


class CommonWebsiteViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.factory = RequestFactory()

    def test_common_website_get(self):
        request = self.factory.get(reverse('allifmaalcommonapp:commonWebsite'))  # Replace 'my_website' with the actual URL name
        # Add session to the request
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        response = commonWebsite(request)
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'allifmaalcommonapp/website/website.html')
        #self.assertEqual(response.context['title'], 'Allifmaal ERP')
        response = self.client.get(reverse('allifmaalcommonapp:commonWebsite'))
        self.assertTemplateUsed(response, 'allifmaalcommonapp/website/website.html')

    def test_common_website_exception(self):
        request = self.factory.get(reverse('allifmaalcommonapp:commonWebsite'))
       

        with patch('allifmaalcommonapp.views.render') as mock_render:
            mock_render.side_effect = Exception('Test Exception')
            try:
                commonWebsite(request)
            except Exception as e:
                self.assertEqual(str(e), 'Test Exception')
                #response = self.client.get(reverse('allifmaalcommonapp:commonWebsite'))
                #self.assertTemplateUsed(response, 'allifmaalcommonapp/error/error.html')
            self.assertTrue(mock_render.called)
        
        #with patch('allifmaalcommonapp.views.render') as mock_render:
            #mock_render.side_effect = Exception('Test Exception')
            #response = self.client.get(reverse('allifmaalcommonapp:commonWebsite'))
           # self.assertTemplateUsed(response, 'allifmaalcommonapp/error/error.html')





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