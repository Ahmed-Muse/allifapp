from django.db import models
from allifmaalusersapp.models import User

class AllifmaalUsersModel(User):
    rights= [
    ('allifmaaladmin','allifmaaladmin'),
    ('allifmaalowner', 'allifmaalowner'),
    ('allifmaalstaff', 'allifmaalstaff'),
    ]
    
    allifmaalcategory= models.CharField(choices=rights, default='allifmaalstaff', max_length=100,null=True,blank=True)
    
   
class AllifmaalUsersLoginModel(models.Model):
    username = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
   
    def __str__(self):
        return self.username

