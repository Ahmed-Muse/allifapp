from django.test import TestCase
from .models import User
from django.db.utils import IntegrityError
from datetime import date
from .models import CommonSectorsModel  # Replace . with your app name

class CommonSectorsModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_common_sectors_creation(self):
        sector = CommonSectorsModel.objects.create(name="Hospitality", owner=self.user,notes="Sector Comments")
        self.assertEqual(sector.name, "Hospitality")
        self.assertEqual(sector.notes, "Sector Comments")
        self.assertEqual(sector.owner, self.user)
        self.assertIsNotNone(sector.date)
        self.assertIsInstance(sector.date, date)
    
    def test_max_lengths(self):
        sector = CommonSectorsModel.objects.create(name="A" * 20, owner=self.user)
        self.assertEqual(len(sector.name), 20)
        sector = CommonSectorsModel.objects.create(name="Test", notes="A" * 50, owner=self.user)
        self.assertEqual(len(sector.notes), 50)

    def test_unique_fields(self):
        CommonSectorsModel.objects.create(name="Unique", owner=self.user)
        with self.assertRaises(IntegrityError):
            CommonSectorsModel.objects.create(name="Unique", owner=self.user)

    def test_blanks_nulls(self):
        sector = CommonSectorsModel.objects.create(name="BlankNotes", notes="", owner=self.user)
        self.assertEqual(sector.notes, "")
        sector2 = CommonSectorsModel.objects.create(name = "NullNotes", notes = None, owner = self.user)
        self.assertIsNone(sector2.notes)
        sector = CommonSectorsModel.objects.create(name="NoOwner", owner=None)
        self.assertIsNone(sector.owner)

    def test_foreignkeys(self):
        sector = CommonSectorsModel.objects.create(name="OwnerTest", owner=self.user)
        self.assertEqual(sector.owner, self.user)
   
    def test_str_representation(self):
        sector = CommonSectorsModel.objects.create(name="TestSector", owner=self.user)
        self.assertEqual(str(sector), "TestSector")
    
    ######################## test for not null fields ##############
    #def test_required_fields_not_blank(self): # this might not work for sqlite.... so use it when dealing others dbs.
        #with self.assertRaises(IntegrityError):
            #CommonSectorsModel.objects.create(name="", owner=self.user)

