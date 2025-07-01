from django.db import models
from django.template.defaultfilters import register, slugify
from uuid import uuid4 
#from django.contrib.auth.models import User
from allifmaalusersapp.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from .constants import PRESCRIPTION_FORMULATIONS, ADMINISTRATION_ROUTES, DOSAGE_UNITS, OCCUPANCY_STATUSES, APPOINTMENT_STATUSES, ADMISSION_STATUSES, REFERRAL_TYPES, REFERRAL_STATUSES, LAB_TEST_STATUSES, IMAGING_TEST_STATUSES, PATIENT_GENDERS, BLOOD_GROUPS, ENCOUNTER_TYPES, MEDICAL_SERVICE_TYPES
from django.urls import reverse
from django.utils import timezone # Make sure to import timezone
from .constants import *
from decimal import Decimal
from django.http.response import HttpResponse, JsonResponse
import uuid 
# --- AuditLog Model (for Signals & Logging Examples) ---
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#################################################### NOTES ###################################
# This database should serve the following sectors
# 1. Healthcare
# 2. Education
# 3. Distribution/Sales
# 4. Hospitality
# 5. Real Estate
# 6. Logistics
# 7. Services
# and the following are the repetitive modules that should be covered.
#   1. Employees - HRM, staff, teachers, doctors, engineers, sales people, accountants etc.
#   2. Customers - customers, students, patients, clients etc
#   3. Suppliers - allmost same for all
#   4. Inventory - all most same for all...some for resale some not like schools inventory such as books, pens etc
#   5. Quotations - all most same for all
#   6. Invoices - all most same for all
#   7. Company Details - almost same for all
#   8. Company Scope - almost same
#   9. System Users - almost same for all
#   10. Procurement Processes - almost same for all
#   11. Assets
#   12. Chart of accounts
#   13. Expenses
#   14. Reports - financial statements, customer statments, supplier statmenets etc.
#   15. Taxes
#   16. Posted documents - invoices, POs, returns etc.
#   17. Salaries - applies to all companies
#   18. Banks
#   19. Tasks
#   20. Departments


# some of the databases may shared 100% like employees while others may be shared partitially like customers.
# we may have various views for various apps but they may share database
# 
# #

# check lenght, ondelete, true/false
class CommonSectorsModel(models.Model):# this is the company  hospitality logistics
    name=models.CharField(max_length=30,blank=False,null=False,unique=True,default="Sector Name",db_index=True)
    notes=models.CharField(max_length=50,blank=True,null=True,default="Sector Comments")
    owner=models.ForeignKey(User,db_index=True, on_delete=models.SET_NULL,blank=True,null=True,related_name="secownr")
    date=models.DateField(blank=True,null=True,auto_now_add=True)
   
    def __str__(self):
        return self.name
   
class CommonDocsFormatModel(models.Model):# this is the company  hospitality logistics
    name=models.CharField(max_length=30,blank=False,null=False,unique=True,default="pdf")
    notes=models.CharField(max_length=50,blank=True,null=True,default="Write Document Type")
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name="docformusr")
    date=models.DateField(blank=True,null=True,auto_now_add=True)
  
    def __str__(self):
        return self.name
class CommonDataSortsModel(models.Model):# this is the company  hospitality logistics
    name=models.CharField(max_length=30,blank=False,null=False,unique=True,default="asc")
    notes=models.CharField(max_length=50,blank=True,null=True,default="Write Document Type")
    owner= models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name="datsortusr")
    date=models.DateField(blank=True,null=True,auto_now_add=True)
   
    def __str__(self):
        return self.name
# this company can be normal companies, hospital, hotels, schools, universities, etc
#################3 Entity/Company Details ################
class CommonCompanyDetailsModel(models.Model):# this is the company
    company=models.CharField(max_length=50,blank=True,null=True,db_index=True)
    legalName=models.CharField(max_length=50,blank=True,null=True,default="CompanyLegalName")
    address=models.CharField(max_length=50,blank=True,null=True)
    companyuid=models.CharField(null=True, blank=True, max_length=250,unique=True)
    companyslug=models.SlugField(max_length=150, unique=True, blank=True, null=True)
    pobox=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    website=models.CharField(max_length=50,blank=True,null=True)
    phone1=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    phone2=models.CharField(max_length=50,blank=True,null=True)
    logo=models.FileField(upload_to='myfiles/',null=True, blank=True)
    owner=models.OneToOneField(User, on_delete=models.SET_NULL,blank=True,null=True,related_name="secrlmown")
    sector=models.ForeignKey(CommonSectorsModel,related_name="secrlmcompcmmnapp",on_delete=models.PROTECT,null=True,blank=False)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    updatedon=models.DateTimeField(blank=True, null=True)
    created_date=models.DateField(null=True, blank=True)
    edit_date=models.DateField(null=True, blank=True)
    can_delete=models.CharField(choices=delete_status, blank=True, null=True,max_length=30,default="undeletable")
    status= models.CharField(choices=entity_status, blank=True, null=True,max_length=30,default="Blocked")

    def __str__(self):
        return str(self.company)
    def save(self, *args, **kwargs):
        if self.companyuid is None:
            self.companyuid=str(uuid4()).split('-')[4]
            self.companyslug=slugify('{} {}'.format(self.legalName, self.companyuid))
        self.companyslug=slugify('{} {}'.format(self.legalName, self.companyuid))#this is what generates the slug
        self.updatedon=timezone.localtime(timezone.now())
        super(CommonCompanyDetailsModel, self).save(*args, **kwargs)

#######33 Branches --- this is needed if a company has more than one branch ################
class CommonDivisionsModel(models.Model):# this is the company
    division=models.CharField(max_length=50,blank=True,null=True)
    legalname=models.CharField(max_length=50,blank=True,null=True,default="CompanyDvsnLegalName")
    address=models.CharField(max_length=50,blank=True,null=True)
    divisionuid=models.CharField(null=True, blank=True, max_length=100,unique=True)
    divisionslug=models.SlugField(max_length=250, unique=True, blank=True, null=True)
    pobox=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    phone=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name="owncmpndvsn")
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="dvsncmpny",on_delete=models.CASCADE,null=True,blank=False)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    updatedon=models.DateTimeField(blank=True, null=True)
    created_date=models.DateField(null=True, blank=True)
    edit_date=models.DateField(null=True, blank=True)
    comments=models.TextField(max_length=100, help_text="Enter a brief description of the division",blank=True,null=True)
    class Meta:
        # ensures that the same value is not repeated in the same company
        unique_together = ('company', 'division')
    def __str__(self):
        return str(self.division)
    def save(self, *args, **kwargs):
        if self.divisionuid is None:
            self.divisionuid=str(uuid4()).split('-')[4]
            self.divisionslug=slugify('{} {}'.format(self.legalname, self.divisionuid))
        self.divisionslug=slugify('{} {}'.format(self.legalname, self.divisionuid))#this is what generates the slug
        self.updatedon=timezone.localtime(timezone.now())
        super(CommonDivisionsModel, self).save(*args, **kwargs)

#######33 Branches --- this is needed if a company has more than one branch ################
class CommonBranchesModel(models.Model):# this is the company
    branch=models.CharField(max_length=50,blank=True,null=True)
    legalname=models.CharField(max_length=50,blank=True,null=True,default="CompanyBranchLegalName")
    address=models.CharField(max_length=50,blank=True,null=True)
    branchuid =models.CharField(null=True, blank=True, max_length=100,unique=True)
    branchslug =models.SlugField(max_length=150, unique=True, blank=True, null=True)
    pobox=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    phone=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name="owncmpnbrnch")
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="brnchcmpny",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvnscmpny",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    updatedon=models.DateTimeField(blank=True, null=True)
    created_date=models.DateField(null=True, blank=True)
    edit_date=models.DateField(null=True, blank=True)
    #class Meta:
        # ensures that the same value is not repeated in the same company
        #unique_together = ('branch', 'division','company')

    def __str__(self):
        return str(self.branch)
    def save(self, *args, **kwargs):
        if self.branchuid is None:
            self.branchuid=str(uuid4()).split('-')[4]
            self.branchslug=slugify('{} {}'.format(self.legalname, self.branchuid))
        self.branchslug=slugify('{} {}'.format(self.legalname, self.branchuid))#this is what generates the slug
        self.updatedon=timezone.localtime(timezone.now())
        super(CommonBranchesModel, self).save(*args, **kwargs)

########################## Common departments ##########################3
class CommonDepartmentsModel(models.Model):
    department=models.CharField(max_length=50,blank=False,null=True,unique=False)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="usrdprmnt",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpdprmnt",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dpmntdvsn",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="dpmntbrnch",on_delete=models.SET_NULL,null=True,blank=True)
    comments=models.CharField(null=True, blank=True, max_length=30)
    pobox=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    phone=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    legalname=models.CharField(max_length=50,blank=True,null=True,default="CompanyDepartmentLegalName")
    address=models.CharField(max_length=50,blank=True,null=True)
    departmentuid=models.CharField(null=True, blank=True, max_length=100,unique=True)
    departmentslug=models.SlugField(max_length=250, unique=True, blank=True, null=True)
    updatedon=models.DateTimeField(blank=True, null=True)
    #class Meta:
        # ensures that the same value is not repeated in the same company
        #unique_together = ('company', 'division','branch')
    def __str__(self):
        return str(self.department)
    
    def save(self, *args, **kwargs):
        if self.departmentuid is None:
            self.departmentuid=str(uuid4()).split('-')[4]
            self.departmentslug=slugify('{} {}'.format(self.legalname, self.departmentuid))
        self.departmentslug=slugify('{} {}'.format(self.legalname, self.departmentuid))#this is what generates the slug
        self.updatedon=timezone.localtime(timezone.now())
        super(CommonDepartmentsModel, self).save(*args, **kwargs)


class CommonOperationYearsModel(models.Model):
    """
    defines the opreational/fiscal/academic year..
    
    """
    description= models.TextField(null=True, blank=True,default='Description')
    comments=models.TextField(blank=True,null=True, default='Comments')
    date=models.DateField(auto_now_add=True,blank=True,null=True)
    starts=models.DateTimeField(blank=True,null=True,default=timezone.now)
    ends=models.DateTimeField(blank=True,null=True,default=timezone.now)
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='operation_year_updated')
    year=models.CharField(max_length=50,blank=True,default="Operation Year",null=True,unique=False,help_text="e.g., 2023-2024")
    is_current=models.CharField(choices=operation_year_options,max_length=50,blank=True,null=True,default="Current")
    owner=models.ForeignKey(User, related_name="ownr_operation_year",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmp_operation_year",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_operation_year",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_operation_year",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dept_operation_year",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return str(self.year)
    
class CommonOperationYearTermsModel(models.Model):
    """
    this model captures operational year sections like terms, semisters, quarters ...etc
    """
    name=models.CharField(max_length=30,blank=True,null=True,default="Operation Term")
    date=models.DateField(auto_now_add=True,blank=True,null=True)
    description= models.TextField(null=True, blank=True,default='Description')
    comments=models.TextField(blank=True,null=True, default='Comments')
    starts=models.DateTimeField(blank=True,null=True,default=timezone.now)
    ends=models.DateTimeField(blank=True,null=True,default=timezone.now)
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='operation_term_updated')
    year=models.CharField(max_length=50,blank=True,default="Operation Year",null=True,unique=False,help_text="e.g., 2023-2024")
    
    owner=models.ForeignKey(User, related_name="ownr_operation_term",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmp_operation_term",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_operation_term",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_operation_term",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dept_operation_term",on_delete=models.SET_NULL,null=True,blank=True)
    
    operation_year=models.ForeignKey(CommonOperationYearsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='terms_operation_year')
   
   
    def __str__(self):
        return str(self.name)


#############################################################
# Abstract Base Class for Common Organizational Fields
class CommonBaseModel(models.Model):
    """
    An abstract base class that provides common organizational fields
    like company, division, branch, department, owner, and creation date.
    Models inheriting from this will get these fields directly in their table.
    Also Use '+' for related_name in abstract base classes to prevent reverse accessor clashes --- The related name will not be created on the related object.
    """
    owner=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='+')
    company=models.ForeignKey(CommonCompanyDetailsModel,on_delete=models.CASCADE,null=True,blank=True,related_name='+')
    division=models.ForeignKey(CommonDivisionsModel,on_delete=models.SET_NULL,null=True,blank=True,related_name='+')
    branch=models.ForeignKey(CommonBranchesModel,on_delete=models.SET_NULL,null=True,blank=True,related_name='+')
    department=models.ForeignKey(CommonDepartmentsModel,on_delete=models.SET_NULL,null=True,blank=True,related_name='+')
    name=models.CharField(max_length=30,blank=True,null=True,default="Name")
    number=models.CharField(max_length=50,blank=True,null=True, unique=False, help_text="Unique code for the program, e.g., BSCIT")
    date=models.DateField(auto_now_add=True,blank=True,null=True)
    description= models.TextField(null=True, blank=True,default='Description')
    quantity=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    comments=models.TextField(blank=True,null=True, default='Comments')
    starts=models.DateTimeField(blank=True,null=True,default=timezone.now)
    ends=models.DateTimeField(blank=True,null=True,default=timezone.now)
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
    operation_year=models.ForeignKey(CommonOperationYearsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='+')
    operation_term=models.ForeignKey(CommonOperationYearTermsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='+')
   
    updated_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    #is_current=models.CharField(choices=operation_year_options,max_length=50,blank=True,null=True,default="Current")
    code=models.CharField(max_length=50,blank=True,null=True, unique=True, help_text="Unique code for the program, e.g., BSCIT")
    balance=models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True,default=0.00)
    status=models.CharField(max_length=50, choices=BASE_MODEL_STATUS_CHOICES, default='Draft',null=True,blank=True)
    priority=models.CharField(max_length=50, choices=PRIORITY_LEVELS, default='Normal',null=True,blank=True)
    delete_status=models.CharField(choices=delete_status, blank=True, null=True,max_length=30,default="Deletable")
    #universally unique identifier. Excellent for public-facing IDs, preventing enumeration attacks, and multi-database syncing. You often don't want this to be editable by users.
    #If your uniqueId is intended to be a UUID, consider switching its type to models.UUIDField.
    uuid=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True,null=True,blank=True)
    reference=models.CharField(max_length=100, default='reference',blank=True, null=True, db_index=True, help_text="An optional identifier from an external system or an internal reference code.")
    class Meta:
        abstract = True # This is the crucial line that makes it an abstract base class

class CommonCompanyScopeModel(CommonBaseModel):# this is the company  hospitality logistics
    scope_type=models.CharField(max_length=30,choices=SCOPE_TYPES,blank=True,null=True,)
    scope_resources=models.TextField(blank=True,null=True,help_text="Resources required by this particular scope")
    scope_constraints=models.TextField(blank=True,null=True,)
    scope_assumptions=models.TextField(blank=True,null=True)
    scope_exclusions = models.TextField(blank=True,null=True,help_text="Specific items, features, or activities that are explicitly excluded from this scope.")
    scope_stakeholders = models.TextField(blank=True,null=True,help_text="Key individuals or groups affected by or having an interest in this scope.")
    scope_risks=models.TextField(blank=True,null=True,help_text="A summary of identified risks associated with this scope.")

    def __str__(self):
        return self.name


















# taxes...
class CommonTaxParametersModel(CommonBaseModel):
    taxtype=models.CharField(choices=taxoptions, blank=True, max_length=30,default='Default')
    taxrate=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,default=0)
    def __str__(self):
        return f"{self.name} ({self.taxrate}%)"

    def clean(self):
        super().clean() # Call parent clean method
        if self.taxrate is not None and self.taxrate < 0:
            raise ValidationError("Tax Rate cannot be negative")

    class Meta:
        # Principle 3: Fine-Grained Permissions (added here for model-level permission)
        permissions = [
            ("view_tax_parameter", "Can view tax parameter"),
            ("add_tax_parameter", "Can add tax parameter"),
            ("change_tax_parameter", "Can change tax parameter"),
            ("delete_tax_parameter", "Can delete tax parameter"),
        ]



class CommonAuditLogsModel(CommonBaseModel):
    action_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=50) # e.g., 'CREATED', 'UPDATED', 'DELETED', 'LOGIN'
    
    # Generic Foreign Key to link to any model instance
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True) # Store PK as string
    content_object = GenericForeignKey('content_type', 'object_id') # The actual object

    object_repr = models.CharField(max_length=200, null=True, blank=True) # __str__ representation
    change_message = models.TextField(blank=True, null=True) # Details of the change

    class Meta:
        ordering = ['-action_time']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        # Principle 3: Fine-Grained Permissions
        permissions = [
            ("view_audit_log", "Can view audit log entries"),
        ]

    def __str__(self):
        return f"{self.action_type} on {self.object_repr} by {self.user.first_name if self.user else 'System'} at {self.action_time.strftime('%Y-%m-%d %H:%M')}"



class CommonSupplierTaxParametersModel(CommonBaseModel):
    taxtype=models.CharField(choices=taxoptions, blank=True, max_length=30)
    taxrate=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
   
    def __str__(self):
        return str(self.name)
        #return self.taxname +"   "+str(self.taxrate)+str('%')
    def clean(self):
        if self.taxrate<0:
            raise ValidationError("Tax Rate cannot be negative")
        
class CommonCurrenciesModel(CommonBaseModel):
    def __str__(self):
        return str(self.description)


class CommonPaymentTermsModel(CommonBaseModel):
  
    def __str__(self):
        return str(self.description)
    
class CommonUnitsModel(CommonBaseModel):
    def __str__(self):
        return str(self.description)


#########################################3 stock, items, services, subjects categories.. ##############################################
class CommonCategoriesModel(CommonBaseModel):
    """
    Defines the categories of programs/items/subject/services that are offered by a particular entity
    for example:
    Sales...sales, manufacturing, repairs, services contracts etc.
    Education...Bachelor of Science in IT, Diploma in Nursing, PhD in MBA etc.
    Healthcare...General surgery, Maternity, Dental, Checkups etc.
    Hospitality...Accommodation, outdoor catering, spacing letting(malls/apartments),conferences, events etc
    Logistics....travelling, tourism, Hajj,Umrah,Cargo, handling, clearing etc
    Realestate...spacing letting(malls/apartments),property management,property development etc
    Services...consultancy, financial services, audit, legal, accounting etc..
    ....
    another list is as below....
    this defines the item types of various industreis...
    sales... these are Physical Products like solid, gas, chemicals, liquid...
    healthcare...tablets, syrub, injection, vial, powder,Cream/Ointment, medical device, consumable,vaccine, service etc.
    education....subjects, courses, textbooks, stationery item, lab equipment, digital resource, tuition fee etc.
    Realestate... residential, commercial, mixed-use, land parcel, plot, service, lease agrement...
    logistics...Package, Pallet, Container, Freight Unit, spare, Service (Transport), Seat/Ticket...
    hospitality... Standard Room, Deluxe room, Suite, Food, Beverage, drink, Dish (Prepared), Consumable (Guest, toiletries, towels, minibar items), Linen: For bedsheets, tableclothses,
    Service (Hotel such laundry service, room service, concierge, Event Space: For inventoryin....
    Service... documents, software, consultaning hours, training, service ...etc..
    
    """
   
    def __str__(self):
    		return str(self.name) # this will show up in the admin area

###################3 comon codes ##############
class CommonCodesModel(CommonBaseModel):
    """
    this defines the codes used by various entities.....
    sales...codes of various items...
    healthcare...codes of various places, items, staff, wards, rooms, equipment etc
    logistics...codes of airports, cities, items, passengers etc..
    realestates...codes of properties, places, items, equipment etc
    education... codes of places, items, machines, equipment, student registeration numbers etc.
    
    """
   
    class Meta:
        # ensures that the same value is not repeated in the same company
        unique_together = ('company', 'code','name')
    
    def __str__(self):
        return f"{self.code}: {self.name}:"



# #################3 HRM ################    
class CommonEmployeesModel(CommonBaseModel):
    
    firstName=models.CharField(max_length=50,blank=False,null=True)
    lastName=models.CharField(max_length=50,blank=True,null=True)
    middleName=models.CharField(max_length=50,blank=True,null=True)
    gender=models.CharField(max_length=25, blank=True, null=True,choices=gender)
    title=models.CharField(max_length=50,blank=True,null=True)
    education=models.CharField(max_length=50,blank=True,null=True)
    
    salary=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    total_salary_paid=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    salary_payable=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    salary_balance=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    username=models.OneToOneField(User, on_delete=models.CASCADE,related_name="secrlmmemply",null=True)
    uniqueId=models.CharField(null=True, blank=True, max_length=150)
    sysperms=models.CharField(choices=rights, blank=True, null=True,max_length=30,default="staff")
    
    stffslug=models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.firstName)
        
    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId=str(uuid4()).split('-')[4]
            self.stffslug=slugify('{} {} {} {} {}'.format(self.company,self.company.address, self.uniqueId,self.firstName,self.middleName))
        self.stffslug=slugify('{} {} {} {} {}'.format(self.company,self.company.address, self.uniqueId,self.firstName,self.middleName))#this is what generates the slug
        super(CommonEmployeesModel, self).save(*args, **kwargs)

class CommonApproversModel(CommonBaseModel):
   
    approvers=models.ForeignKey(CommonEmployeesModel,null=True,blank=True, related_name='apprvrusrmbmrs',on_delete=models.SET_NULL) # Users in this group
   
    def __str__(self):
        return str(self.approvers)

########################## CHART OF ACCOUNTS ##########################3
class CommonGeneralLedgersModel(CommonBaseModel):
    def __str__(self):
        return str(self.description)

class CommonChartofAccountsModel(CommonBaseModel):
    
    
    category=models.ForeignKey(CommonGeneralLedgersModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='chaccmrln')
   
    statement=models.CharField(choices=chart_of_account_statement_type,max_length=20,blank=True,null=True)
    def __str__(self):
        return str(self.description)

########################## banks #########################
class CommonBanksModel(CommonBaseModel):
    account=models.CharField(max_length=30,blank=True,null=True)
    deposit=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    withdrawal=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    def __str__(self):
        return '{}'.format(self.name)

############################ SHAREHOLDER DEPOSITS AND INVESTMENTS #####################################3
class CommonShareholderBankDepositsModel(CommonBaseModel):
    bank=models.ForeignKey(CommonBanksModel,related_name="depositbankrelnefds",on_delete=models.SET_NULL,blank=False,null=True)
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
   
    equity=models.ForeignKey(CommonChartofAccountsModel,related_name="dpscustrlnmdfd",on_delete=models.SET_NULL,blank=False,null=True)
    asset=models.ForeignKey(CommonChartofAccountsModel, blank=True,null=True,on_delete=models.SET_NULL,related_name='coabnkdpasset')
    
    status=models.CharField(choices=posting_status, default='waiting', max_length=20,blank=True,null=True)
    def __str__(self):
        return '{}'.format(self.description)

######################3 WITHDRAWALS ############33
class CommonBankWithdrawalsModel(CommonBaseModel):
    
    bank=models.ForeignKey(CommonBanksModel,related_name="wthdrbnkrelnm",on_delete=models.SET_NULL,blank=False,null=True)
    amount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    
    asset=models.ForeignKey(CommonChartofAccountsModel, blank=False,null=True,on_delete=models.SET_NULL,related_name='coabnka')
    bankcoa=models.ForeignKey(CommonChartofAccountsModel, blank=False,null=True,on_delete=models.SET_NULL,related_name='coabnkafrm')
    
    def __str__(self):
        return '{}'.format(self.description)


########################## Emails and SMSs #########################
class CommonEmailsModel(CommonBaseModel):
    subject=models.CharField(max_length=255,blank=True,null=True)
    message=models.CharField(max_length=255,blank=True,null=True)
    sender=models.EmailField(max_length=50,blank=True,null=True, default='sender')
    recipient=models.EmailField(max_length=50,blank=True,null=True, default='recipients')
    sender=models.CharField(max_length=50,blank=True,null=True, default='comment')
    
    def __str__(self):
        return '{}'.format(self.subject)


#################3 suppliers ################
class CommonSuppliersModel(CommonBaseModel):
   
    phone=models.CharField(null=True, blank=True, max_length=30)
    email=models.EmailField(null=True, blank=True, max_length=30)
    city=models.CharField(null=True, blank=True, max_length=30)
    address=models.CharField(null=True, blank=True, max_length=30)
    turnover=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    contact=models.CharField(null=True, blank=True, max_length=30)
   
    country=models.CharField(null=True, blank=True, max_length=50)
    
    coverage=models.TextField(max_length=250,blank=True,null=True,default='Insurance')
  
  
    def __str__(self):
        return '{}'.format(self.name)
    
class CommonSupplierPaymentsModel(CommonBaseModel):
    supplier=models.ForeignKey(CommonSuppliersModel,related_name="allifsuprln",on_delete=models.SET_NULL,blank=True,null=True)
    amount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    
    account=models.ForeignKey(CommonChartofAccountsModel,related_name="amesupayrlnm",on_delete=models.SET_NULL,blank=True,null=True)
    mode=models.ForeignKey(CommonPaymentTermsModel, related_name="supplrpymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    posting_status=models.CharField(choices=posting_status, default='waiting', max_length=100,blank=True,null=True)
    
    def __str__(self):
        return '{}'.format(self.supplier)

class CommonSupplierStatementsModel(CommonBaseModel):
    supplier=models.ForeignKey(CommonSuppliersModel,related_name="supstmrl",on_delete=models.CASCADE,blank=True,null=True)
    debit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    credit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    
  
    def __str__(self):
        return '{}'.format(self.supplier)
    
#.... customers .... this include normal customers, students, etc
class CommonCustomersModel(CommonBaseModel):
    uid=models.CharField(null=True, blank=True, max_length=100,unique=True)
    phone=models.CharField(null=True, blank=True, max_length=30)
    email=models.EmailField(null=True, blank=True, max_length=50)
    city=models.CharField(null=True, blank=True, max_length=30)
    address=models.CharField(null=True, blank=True, max_length=30)
    sales=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    turnover=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    contact=models.CharField(null=True, blank=True, max_length=30)
    uniqueId=models.CharField(null=True, blank=True, max_length=100)
    customerslug=models.SlugField(max_length=50, unique=True, blank=True, null=True)
   
    paymentType=models.ForeignKey(CommonPaymentTermsModel, related_name="custmerrpymntrms",on_delete=models.SET_NULL,null=True,blank=True)
    #..... end.... below fields is special for healthcare entities setup....

    #..... start.... below fields is special for educational setup....
    #form=models.ForeignKey(CommonFormsModel,on_delete=models.SET_NULL,blank=True,null=True)
    #className=models.ForeignKey(CommonClassesModel,on_delete=models.SET_NULL,blank=True,null=True)
    course_category=models.ForeignKey(CommonCategoriesModel,blank=True,null=True, on_delete=models.CASCADE, related_name='course_enrollments')
    operation_year=models.ForeignKey(CommonOperationYearsModel, on_delete=models.CASCADE, related_name='year_enrollments',null=True,blank=True)
    term=models.ForeignKey(CommonOperationYearTermsModel, on_delete=models.CASCADE, related_name='term_enrollments',blank=True,null=True)
    enrollment_date=models.DateField(auto_now_add=True,blank=True,null=True)
    client_status=models.CharField(max_length=4, choices=student_status_choices, default='ENR',blank=True,null=True)

     #..... end.... below fields is special for educational setup....
    
    country=models.CharField(null=True, blank=True, max_length=50)
   
    ############################## for medical ######################################
    age=models.CharField(null=True, blank=True, max_length=30)
    nextkin=models.CharField(null=True, blank=True, max_length=30)
    relationship=models.CharField(null=True, blank=True, max_length=30)
    register=models.BooleanField('Mark registered',default=False,blank=True,null=True)
    triaged=models.BooleanField('Mark triaged',default=False,blank=True,null=True)
    seen=models.BooleanField('Mark seen',default=False,blank=True,null=True)
    gender=models.CharField(max_length=25, blank=True, null=True,choices=gender)
    date_of_birth=models.DateField(blank=True,null=True)
    
    blood_group=models.CharField(max_length=3, choices=BLOOD_GROUPS, blank=True, null=True)
    # Storing allergies/conditions as free text initially, but consider ManyToManyField
    # to a catalogue of allergies/conditions for structured data later.
    known_allergies=models.TextField(blank=True, null=True,help_text="List of known allergies (e.g., Penicillin, Peanuts)")
    chronic_conditions = models.TextField(blank=True, null=True,help_text="List of chronic medical conditions (e.g., Diabetes, Hypertension)")
    
    ############### below hospitality specific fields.... ################3
    passport_number = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="Unique ID for guest")
    nationality=models.CharField(max_length=100, blank=True, null=True)
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.customerslug = slugify('{} {}'.format(self.fullName, self.uniqueId))

        self.customerslug = slugify('{} {}'.format(self.fullName, self.uniqueId))#this is what generates the slug
        super(CommonCustomersModel, self).save(*args, **kwargs)
   
class CommonCustomerPaymentsModel(CommonBaseModel):
    customer=models.ForeignKey(CommonCustomersModel,related_name="allifcustpaymentreltedname",on_delete=models.CASCADE,blank=True,null=True)
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    
    mode=models.ForeignKey(CommonPaymentTermsModel, related_name="custmrpymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return '{}'.format(self.customer)

class CommonCustomerStatementsModel(CommonBaseModel):
    customer=models.ForeignKey(CommonCustomersModel,related_name="custstmrlnm",on_delete=models.CASCADE,blank=True,null=True)
    debit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    credit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
   
    def __str__(self):
        return '{}'.format(self.customer)

class CommonLedgerEntriesModel(CommonBaseModel): # this is the journal entries...
    supplier=models.ForeignKey(CommonSuppliersModel,related_name="sppldgentr",on_delete=models.CASCADE,blank=True,null=True)
    customer=models.ForeignKey(CommonCustomersModel,related_name="cstmldgentr",on_delete=models.CASCADE,blank=True,null=True)
    staff=models.ForeignKey(CommonEmployeesModel,related_name="empldgentr",on_delete=models.CASCADE,blank=True,null=True)
    debit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    credit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    originalamount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    newamount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    ledgowner=models.CharField(choices=ledgerentryowner, max_length=50,blank=True,default="staff")
   
    def __str__(self):
        return '{}'.format(self.comments)
 

class CommonAssetsModel(CommonBaseModel):
    """
    thi can represent a normal asset to any company...vehicles, equipment, properties etc...
    
    The asset can be a building/property for the entity... for instance in:
    sales... building that the company may own or reside in
    healthcare...this is the hospital building that contains the wards and other sections of operation
    realestate...these are the properties/buildings of the company...like appartments etc.
    education... this represents dormitaries or other buildings of the school
    logistics and other sectors....building owned/managed by the company
    """
    
    supplier=models.ForeignKey(CommonSuppliersModel,related_name="suplporelnmeasset",on_delete=models.SET_NULL,blank=False,null=True)
    terms=models.ForeignKey(CommonPaymentTermsModel, related_name="asstpymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    asset_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='cmassetrl')
    cost_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='cstasschac')
    equipment_name=models.CharField(max_length=50, blank=True, null=True)
    description=models.CharField(max_length=50,blank=False,null=True)
    years_depreciated=models.CharField(max_length=30,blank=False,null=True)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    value=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    sum_years_digits=models.IntegerField(blank=True,null=True,default=0)
    asset_life=models.IntegerField(blank=True,null=True,default=0)
    asset_age=models.IntegerField(blank=True,null=True,default=0)
    annual_value_drops=models.CharField(max_length=3000,blank=True,null=True)
    life=models.IntegerField(blank=True,null=True,default=0)
    days_in_use=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    salvage_value=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    current_value=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    deposit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    lifespan=models.CharField(max_length=30,blank=True,null=True)
    acquired=models.DateField(blank=True, null=True)
    per_day_value_drop=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,default=0)
    expires=models.DateField(blank=True, null=True)
    annual_depreciation_rate=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,default=0)
    
    asset_status=models.CharField(choices=asset_current_status,max_length=20,blank=True,null=True)
    depreciation=models.CharField(choices=depreciation_method,max_length=50,blank=True,null=True)
    depreciated_by=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    
    category=models.ForeignKey(CommonCategoriesModel, related_name="assetcat",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, blank=True, null=True,on_delete=models.SET_NULL,related_name='asstdprmtn')
    employee_in_charge=models.ForeignKey(CommonEmployeesModel, blank=True, null=True,on_delete=models.SET_NULL,related_name='asstemply')
   
    maker_name=models.CharField(max_length=50, blank=True, null=True)
    equipment_model=models.CharField(max_length=50, blank=True, null=True)
    manufactured_year=models.CharField(max_length=30, blank=True, null=True)
    equipment_status=models.CharField(max_length=50, blank=True, null=True,choices=equipment_status_options)
   
    starting_odometer=models.CharField(default=0,blank=True,null=True,max_length=250)
    primary_meter=models.CharField(max_length=30, blank=True, null=True,choices=primary_meter_options,default='Kilometers')
    
    oil_type=models.CharField(max_length=30, blank=True, null=True,choices=oil_options)
    oil_capacity=models.CharField(blank=True,null=True,max_length=30)
   
    energy_usage= models.CharField(null=True, blank=True,default=0,max_length=250)
    
    plate_number=models.CharField(max_length=50, unique=False,null=True,blank=True)
   
    capacity_kg=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Carrying capacity in kilograms")
  
    last_service_date=models.DateField(blank=True, null=True)
    next_service_due=models.DateField(blank=True, null=True)
   
    def __str__(self):
        return str(self.description)
    @property
    def asset_total_amount(self):
        assetamount=self.quantity*self.value
        return assetamount

#########################################3 SPACES ##############################################

class CommonSpacesModel(CommonBaseModel):
    """
    It represents any definable, usable, and often bookable/assignable unit or area within a building or property.
    This can be a hotel room, halls, a hospital wards, a classrooms, an office, an apartment, a restaurant table, an event hall, a storage bay etc.
    """
   
    asset=models.ForeignKey(CommonAssetsModel, related_name="asset_space", on_delete=models.SET_NULL, null=True, blank=True)
   
    number_of_units=models.CharField(max_length=50,blank=True,null=True)
    
    space_type=models.CharField(max_length=250,blank=True,null=True, choices=PROPERTY_TYPES, default='AVAIL')
    space_floor=models.PositiveSmallIntegerField(choices=FLOOR_CHOICES, blank=True, null=True)
    current_status = models.CharField(max_length=250,blank=True,null=True, choices=CURRENT_STATUS_CHOICES, default='AVAIL')
    base_price_per_night=models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2)
    monthly_rent=models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2)
    max_occupancy=models.CharField(max_length=100,blank=True,null=True)
    amenities=models.CharField(max_length=250,blank=True,null=True)
    number_of_bedrooms=models.CharField(max_length=100,blank=True,null=True)
    number_of_bathrooms=models.CharField(max_length=100,blank=True,null=True)
    address=models.TextField(blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    capacity=models.CharField(max_length=100,blank=True,null=True)
    emplyee_in_charge=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_warehouses')
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return str(self.name)


class CommonSpaceUnitsModel(CommonBaseModel):
    """
    this defines the sub-units of available spaces....
    sales... office rooms, cubicles, etc
    healthcare...rooms, beds, etc
    education...rooms, beds, etc
    realestates...rooms,beds, etc
    
    """
    
    space=models.ForeignKey(CommonSpacesModel, related_name="units_space", on_delete=models.SET_NULL, null=True, blank=True)
    
    space_type=models.CharField(max_length=250,blank=True,null=True, choices=PROPERTY_TYPES, default='AVAIL')
    space_floor=models.PositiveSmallIntegerField(choices=FLOOR_CHOICES, blank=True, null=True)
    
    current_status = models.CharField(max_length=250,blank=True,null=True, choices=CURRENT_STATUS_CHOICES, default='AVAIL')
    
    base_price_per_night=models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2)
    monthly_rent=models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2)
    
    unitcost=models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2)
    unitprice=models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2)
    rooms=models.CharField(max_length=100,blank=True,null=True)
    washrooms=models.CharField(max_length=100,blank=True,null=True)
    
    max_occupancy=models.CharField(max_length=100,blank=True,null=True)
    amenities=models.CharField(max_length=100,blank=True,null=True)
   
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
    
    capacity=models.CharField(max_length=100,blank=True,null=True)
    emplyee_in_charge=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='speces_units_staff')
   
    unit_type=models.CharField(max_length=10,blank=True,null=True, choices=PROPERTY_UNIT_TYPES)
    
    area_sqm=models.CharField(max_length=100,blank=True,null=True)
   
    def __str__(self):
        return str(self.name)


##################3 EXPENSES ###########################     
class CommonExpensesModel(CommonBaseModel):
    expense_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True, on_delete=models.SET_NULL,related_name='coaexprelnamepaytocmm')
    supplier=models.ForeignKey(CommonSuppliersModel, blank=False, null=True, on_delete=models.SET_NULL,related_name='expsupprelanmeconcmm')
    mode=models.ForeignKey(CommonPaymentTermsModel, related_name="expnspymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
   
    def __str__(self):
        return str(self.description)
   
class CommonStocksModel(CommonBaseModel):
    
    """
    Defines individual courses/subjects/services/goods within a program that are offered by a particular entity
    for example:
    Sales...selling of various items, item repairs, consultancy etc
    Education...sciences, math, electrical current, strenghth of materials, dental surgery etc..
    Healthcare...general consultations, dental washing, maternity and delivery, heart surgery etc.
    Hospitality...Accommodation, outdoor catering, room bookings,conferences, events etc
    Logistics....ticketing, cargo shipment, cargo handling
    Realestate...letting spaces, building management, BMS
    Services...consultancy, financial services, auditing, legal services, accounting services etc..
    
    
    """
    category=models.ForeignKey(CommonCategoriesModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='catinvtconrlnm')
    
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    buyingPrice=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    unitcost=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    standardUnitCost=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    unitPrice=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
   
    criticalnumber=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    inventory_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='coainvrelnm')
    income_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='coaincomerelnm')
    expense_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='coaexprelnm')
    
    taxrate=models.ForeignKey(CommonTaxParametersModel,related_name="stktxrte",on_delete=models.SET_NULL,null=True,blank=True)
    suppliertaxrate=models.ForeignKey(CommonSupplierTaxParametersModel,related_name="supplrstktxrte",on_delete=models.SET_NULL,null=True,blank=True)
    warehouse=models.ForeignKey(CommonSpacesModel,related_name="stckwarehouse",on_delete=models.SET_NULL,null=True,blank=True)
    total_units_sold=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
   
    weight=models.CharField(blank=True,null=True,default="weight",max_length=250)
    length=models.CharField(blank=True,null=True,default="length",max_length=250)
    width=models.CharField(blank=True,null=True,default="width",max_length=250)
    height=models.CharField(blank=True,null=True,default="height",max_length=250)
    expires=models.DateField(blank=True, null=True)
    
    # this field helps a lot.. for instance when invoicing, it will only affect current stock if it  is a physical item
    # if it is service, it will invoice but it will not affect the current stock as it is intangible
    item_state=models.CharField(choices=item_in_physical_state_or_service,max_length=50,blank=True,null=True,default="Current")
    normal_range=models.CharField(max_length=250, blank=True, null=True,help_text="General normal range information for this test (e.g., '70-110 mg/dL').")
    units=models.ForeignKey(CommonUnitsModel,related_name="unit_of_measure_stocks",on_delete=models.SET_NULL,null=True,blank=True)
    
    class Meta:
        # THIS IS THE CRUCIAL ADDITION/CONFIRMATION
        unique_together = ('company', 'number', 'warehouse')
        
    def __str__(self):
    		return str(self.description) # this will show up in the admin area

class CommonSpaceItemsModel(CommonBaseModel):
    space=models.ForeignKey(CommonSpacesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='wrhseitms')
    items=models.ForeignKey(CommonStocksModel,blank=False,null=False, on_delete=models.CASCADE,related_name='wrhseitemsstck')
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    class Meta:
        # THIS IS THE CRUCIAL ADDITION/CONFIRMATION
        unique_together = ('items', 'space')
    def __str__(self) :
        return str(self.items)

#########################################3 STOCK ##############################################
class CommonStockTransferOrdersModel(CommonBaseModel):
   
    from_store=models.ForeignKey(CommonSpacesModel,related_name="frmintcmpstcktrnsfrs",on_delete=models.SET_NULL,null=True,blank=True)
    to_store=models.ForeignKey(CommonSpacesModel,related_name="tointcmpstcktrnsfrs",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
    		return str(self.number) # this will show up in the admin area

class CommonStockTransferOrderItemsModel(CommonBaseModel):
    items=models.ForeignKey(CommonStocksModel,related_name="stcktrnsfordrlns",on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
   
    trans_ord_items_con=models.ForeignKey(CommonStockTransferOrdersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='poitrelname')
  
    def __str__(self):
        return '{}'.format(self.items)
    #below calculates the total selling price for the model


################# TRANSACTIONS SECTION ############3

class CommonTransactionsModel(CommonBaseModel):# very important model
    """
    healthcare....Represents a single visit or interaction a patient has with the healthcare facility.
    This acts as the central hub for all clinical activities during that specific encounter.
    sales... can represent sales orders, sales requisitions etc...
    education...can act as an accademic year file for each student, an exam events, fees payment event etc
    services... service order to customers, maintenance orders...
    realestate.... can act normal sales order when selling rents, properties, services,renting, monthyly rent payments etc..
    hospitality... can act as guest hosting event, customer orders from restaurents... etc...
    """
    
    
    # general fields,,
    
    employee_in_charge=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="encounters_as_primary_doctor",help_text="The main employee attending this encounter.")
    customer=models.ForeignKey(CommonCustomersModel, on_delete=models.SET_NULL,blank=True,null=True, related_name="custmtransrlnme",help_text="The customer associated with this encounter.")
    
   
    payment_mode=models.ForeignKey(CommonPaymentTermsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='terms_payment_mode_trans')
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    def __str__(self):
        return str(self.customer)

class CommonTransactionItemsModel(CommonBaseModel):
    """
    Defines general transaction items...
    sales...can be used for sales orders, stock adjustments, reservations, raise requisitions of materials, project management etc...
    Healthcare...can be used for doctor assessments on patients,triage by nurses, lab orders etc...
    for instance doctor can write test for maleria, typhoid, CBC ... this means that the 
    stock will represent in this case the services of the hospital...etc...
    Education...can be used student assessments (e.g., Quizzes, Exams, Assignments), course registration, material orders like books issued to students.
    for instance, lecturer can test for physics, math etc
    Logistics..this can be used as adding items to a shipment... so the transaction model represents,Shipping Orders, Freight Invoices, Customs Declarations, Fuel Consumption Logs.
    a shipment order, then this adds the particular items that shipment......
    Realestate...the transaction order can represnt a service to customer then these adds the particulars,Lease Agreements, Rent Invoices, Maintenance Work Orders, Property Sale Contracts
    of that service... for instance, the transaction initiated is April rent and in the list of item
    you add the appril rent as an item....
    Service...can be used to add service items like consultancy, viewing, valuation to the service order,Service Contracts, Project Invoices, Support Tickets, Time Logs.
    hospitality... restaurant is order then add items like tea, milk, rice,Guest Check-ins, Guest Folios (Bills), Restaurant Bills, Event Bookings.  etc....
    for hotels is adding items to guest order......
    .....
    healthcare... doctor uses this as lab tests... he can select and test for maleria, cbc, typhoid etc....
    """
    # general fields......
    trans_number=models.ForeignKey(CommonTransactionsModel, on_delete=models.CASCADE, related_name="mdclrcdobsv", blank=True, null=True,help_text="The encounter this triage record belongs to.")
    items=models.ForeignKey(CommonStocksModel,blank=True,null=True, on_delete=models.CASCADE, related_name="patient_orders",help_text="The type of lab test ordered.")
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    #unitcost=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    #unitprice=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
   
    def __str__(self):
        return str(self.items)

class CommonSpaceBookingItemsModel(CommonBaseModel):
    
    
    """
    this defines the actual renting/leasing/occupying of the given above spaces...
    for instance in:
    sales....booking/renting/leasing of any space the entity may own...
    healthcare... ward booking/renting/leasing/occupying...this can also mean booking of doctors or equipment to be used...
    education...booking of any space/room/hostel/apartment etc that the education entity may own and want to use for operations
    like exams, events etc or to charge the use of these spaces like rooms, storages, parkings etc.
    realestate...renting/leasing of apartments, rooms, parkings, stores, stalls, malls etc.
    hospitality... hotel rooms by guests, halls for conferences/weddings, restaurants, cubicles etc.
    logistics/service... same as sales
    
    """
    trans_number=models.ForeignKey(CommonTransactionsModel, related_name="trans_bookings_items", on_delete=models.CASCADE, null=True, blank=True)
    space=models.ForeignKey(CommonSpacesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings') # Nullable if room not assigned yet
    space_unit=models.ForeignKey(CommonSpaceUnitsModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings_space_unit') # Nullable if room not assigned yet
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    
    def __str__(self):
        return str(self.space_unit)
    @property
    def space_allocation_amount(self):
        booking_amount=self.quantity * self.space_unit.unitprice
        return booking_amount


class CommonProgressModel(CommonBaseModel):
    """
    this can be used to record various progresses of customers, staff, students, patients etc..
    Records continuous or periodic vital signs for a patient during an visit or admision.
    healthcare...patient records, patient progress, like nurses can use this to record vital signs...
    education... teachers can use this to record student progress
    realestate...to record customer related progress like renting, maintenances etc.
    hospitality...can be used to record guest progress,like their stayings..
    logistics...shipment progress record....
    sales...item progress record...
    services...service progress record...
    """
    
    trans_number=models.ForeignKey(CommonTransactionsModel, on_delete=models.CASCADE, related_name="vital_signs", blank=True, null=True,help_text="The encounter this vital signs record belongs to.")
    
    recorded_on = models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of measurement
   
    def __str__(self):
        return str(self.trans_number.customer)
    

    
################################## PURCHASES ###########3

class CommonPurchaseOrdersModel(CommonBaseModel):
    class Status(models.TextChoices): # <--- Define choices using TextChoices
        DRAFT = 'Draft', 'Draft'
        PENDING_APPROVAL = 'Pending Approval', 'Pending Approval'
        APPROVED = 'Approved', 'Approved'
        ISSUED = 'Issued', 'Issued (GIN Created)'
        RECEIVED = 'Received', 'Received (GRN Created)'
        CANCELLED = 'Cancelled', 'Cancelled'

    
    uplift=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=2)
    
    supplier=models.ForeignKey(CommonSuppliersModel,related_name="suplporelnme",on_delete=models.SET_NULL,blank=False,null=True)
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
   
    taxamount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    misccosts=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    grandtotal=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    amounttaxincl=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    posting_po_status=models.CharField(choices=posting_status, default='waiting', max_length=100,blank=True,null=True)
    
    payment_terms=models.ForeignKey(CommonPaymentTermsModel, related_name="popymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    delivery=models.CharField(null=True, blank=True, max_length=100)
    currency=models.ForeignKey(CommonCurrenciesModel, related_name="crrncypo",on_delete=models.SET_NULL,null=True,blank=True)
    taxrate=models.ForeignKey(CommonSupplierTaxParametersModel,related_name="sppltxrt",on_delete=models.SET_NULL,blank=True,null=True)
    approval_status= models.CharField(max_length=50, choices=Status.choices, default=Status.DRAFT) 
    def __str__(self):
        return str(self.number)

class CommonPurchaseOrderItemsModel(CommonBaseModel):
    items=models.ForeignKey(CommonStocksModel,related_name="poitemrallirelnm",on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    unitcost=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    po_item_con= models.ForeignKey(CommonPurchaseOrdersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='poitrelname')
    taxRate=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    discount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,default=0)
    def __str__(self):
        return '{}'.format(self.items)
    #below calculates the total selling price for the model
    @property
    def purchase_order_amount(self):
        po_amount=self.quantity * self.unitcost
        return po_amount
    @property
    def po_tax_amount(self):
        potaxamount=self.quantity*self.unitcost*(self.items.suppliertaxrate.taxrate/100)
        return potaxamount
    

class CommonPurchaseOrderMiscCostsModel(CommonBaseModel):
    supplier=models.ForeignKey(CommonSuppliersModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='suppmiscrlnme')
    
    unitcost=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    po_misc_cost_con= models.ForeignKey(CommonPurchaseOrdersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='pomiscrlnm')
    
    def __str__(self):
        return '{}'.format(self.description)
    @property
    def purchase_order_misc_cost(self):
        po_misc_cost=self.quantity * self.unitcost
        return po_misc_cost


################################3 QUOTES ###########################3
class CommonQuotesModel(CommonBaseModel):
   
    customer=models.ForeignKey(CommonCustomersModel,related_name="allifrelatcustquote",on_delete=models.SET_NULL,blank=True,null=True)
    prospect=models.CharField(choices=prospects, default='Default', max_length=20)
    
    total=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    totalwithtax=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    totalwithdiscount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discount=models.CharField(choices=givediscount, default='No', max_length=20)
    tax=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discountValue= models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    salestax=models.ForeignKey(CommonTaxParametersModel,related_name="txqr",on_delete=models.SET_NULL,blank=True,null=True)
    taxAmount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discountAmount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    
    grandtotal=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    payment_terms=models.ForeignKey(CommonPaymentTermsModel, related_name="qtesspymntermdd",on_delete=models.SET_NULL,null=True,blank=True)
    delivery=models.CharField(null=True, blank=True, max_length=100)
    currency=models.ForeignKey(CommonCurrenciesModel, related_name="crrncyqtes",on_delete=models.SET_NULL,null=True,blank=True)
   
    def __str__(self):
        return '{}'.format(self.number)
 
class CommonQuoteItemsModel(CommonBaseModel):
    items=models.ForeignKey('CommonStocksModel',related_name="allifquoteitemdescrelatednm",on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    allifquoteitemconnector= models.ForeignKey(CommonQuotesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='allifquoteitemrelated')
    
    def __str__(self):
        return '{}'.format(self.items)
    #below calculates the total selling price for the model
    @property
    def quote_selling_price(self):
        selling_price=self.quantity * self.items.unitPrice
        return selling_price
    @property
    def quote_selling_price_with_discount(self):
        if self.discount!=None:
            selling_price_with_disc=(self.quantity * self.items.unitPrice)*(1-(self.discount/100))
        else:
            selling_price_with_disc=(self.quantity * self.items.unitPrice)
        return selling_price_with_disc
    @property
    def quote_tax_amount(self):
        qtetaxamount=self.quantity* self.items.unitPrice*(1-(self.discount/100))*(self.items.taxrate.taxrate/100)
        return qtetaxamount

########################### INVOICES ################################
class CommonInvoicesModel(CommonBaseModel):
   
    customer=models.ForeignKey(CommonCustomersModel,related_name="allifrelatcustinvce",on_delete=models.SET_NULL,blank=True,null=True)
    inv_status=models.CharField(blank=True,null=True,choices=invoiceStatus, default='Current', max_length=20)
    
    total=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    totalwithtax=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    totalwithdiscount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discount=models.CharField(choices=givediscount, default='No', max_length=20)
    tax=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discountValue=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    salestax=models.ForeignKey(CommonTaxParametersModel,related_name="txinvce",on_delete=models.SET_NULL,blank=True,null=True)
    taxAmount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discountAmount= models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    
    grandtotal=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    invoice_due_Date=models.DateField(null=True, blank=True)
    invoice_terms=models.ForeignKey(CommonPaymentTermsModel, related_name="invpymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    invoice_status=models.CharField(choices=invoiceStatus, default='Current', max_length=20)
    invoice_currency=models.ForeignKey(CommonCurrenciesModel, related_name="crrncinvoice",on_delete=models.SET_NULL,null=True,blank=True)
    invoice_comments=models.CharField(blank=True,null=True,default='invoice',max_length=20)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    invoice_total=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    posting_inv_status=models.CharField(choices=posting_status, default='waiting', max_length=100,blank=True,null=True)
    invoice_items_total_cost=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    invoice_gross_profit=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    invoice_posting_date=models.DateField(null=True, blank=True)

    payment_terms=models.ForeignKey(CommonPaymentTermsModel, related_name="invpymnt",on_delete=models.SET_NULL,null=True,blank=True)
    delivery=models.CharField(null=True, blank=True, max_length=100)
    currency=models.ForeignKey(CommonCurrenciesModel, related_name="crrncinv",on_delete=models.SET_NULL,null=True,blank=True)
   
    def __str__(self):
        return '{}'.format(self.number)
    """
    def save(self, *args, **kwargs):
        self.balance_due = self.amount_due - self.amount_paid
        # Update CommonInvoice status based on payment
        if self.balance_due <= 0 and self.status != 'PAID':
            self.status = 'PAID'
            if self.common_invoice and self.common_invoice.status != 'Paid':
                self.common_invoice.status = 'Paid'
                self.common_invoice.save()
        elif self.amount_paid > 0 and self.balance_due > 0 and self.status != 'PARTIAL':
            self.status = 'PARTIAL'
            if self.common_invoice and self.common_invoice.status != 'Partial':
                self.common_invoice.status = 'Partial'
                self.common_invoice.save()
        elif self.amount_paid == 0 and self.status != 'PENDING':
             self.status = 'PENDING'
             if self.common_invoice and self.common_invoice.status != 'Pending':
                self.common_invoice.status = 'Pending'
                self.common_invoice.save()

        # Create/Update the CommonInvoice
        if not self.pk or not self.common_invoice: # If new invoice or common_invoice not linked
            common_invoice_instance = CommonInvoicesModel(
                company=self.company,
                owner=self.owner,
                customer=self.booking.guest.customer_profile, # Link to the common customer
                amount=self.amount_due,
                tax_amount=Decimal('0.00'), # Adjust if applicable
                net_amount=self.amount_due,
                balance_due=self.amount_due,
                invoice_date=self.invoice_date or timezone.now().date(),
                due_date=self.due_date,
                status=self.status,
            )
            common_invoice_instance.save()
            self.common_invoice = common_invoice_instance
        else: # If existing invoice, update common_invoice
            if self.common_invoice:
                self.common_invoice.amount = self.amount_due
                self.common_invoice.net_amount = self.amount_due
                self.common_invoice.balance_due = self.balance_due
                self.common_invoice.status = self.status # Keep status in sync
                self.common_invoice.save()

        super().save(*args, **kwargs)
        """
 
class CommonInvoiceItemsModel(CommonBaseModel):
    items=models.ForeignKey(CommonStocksModel,related_name="invitmstckrlnm",on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    allifinvitemconnector= models.ForeignKey(CommonInvoicesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='invitmsrelnm')
    
    def __str__(self):
        return '{}'.format(self.items)
    #below calculates the total selling price for the model
    @property
    def invoice_selling_price(self):
        selling_price=self.quantity * self.items.unitPrice
        return selling_price
    @property
    def invoice_selling_price_with_discount(self):
        if self.discount!=None:
            selling_price_with_disc=(self.quantity * self.items.unitPrice)*(1-(self.discount/100))
        else:
            selling_price_with_disc=(self.quantity * self.items.unitPrice)
        return selling_price_with_disc
    @property
    def invoice_tax_amount(self):
        qtetaxamount=self.quantity* self.items.unitPrice*(1-(self.discount/100))*(self.items.taxrate.taxrate/100)
        return qtetaxamount


################################3 Credit note ######################
# models.py (Credit Note related - NO SIGNIFICANT CHANGE, as it already applies to one company)

# Assuming existing: Company, Customer, Product, Invoice (Sales Invoice), Location
# And existing ChartOfAccount, JournalEntry, JournalEntryLine

class CommonCreditNotesModel(CommonBaseModel):
    customer=models.ForeignKey(CommonCustomersModel, on_delete=models.SET_NULL, related_name='cstmcrdtnot',null=True,blank=True)
    original_invoice=models.ForeignKey(CommonInvoicesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='credtnorgninv')
    
    total_amount=models.DecimalField(max_digits=30, decimal_places=2, default=0.00,null=True,blank=True)
    reasons=models.CharField(max_length=100,blank=False)
    credit_note_status=models.CharField(max_length=50,choices=posting_status, default='waiting',null=True,blank=True)
    
    return_location=models.ForeignKey(CommonSpacesModel, on_delete=models.SET_NULL, null=True, blank=True)
    
    approval_status=models.CharField(max_length=50,choices=approval_status, default='pending',null=True,blank=True)
    def __str__(self):
        return str(self.number)

class CommonCreditNoteItemsModel(CommonBaseModel):
    credit_note=models.ForeignKey(CommonCreditNotesModel, on_delete=models.CASCADE, related_name='crdntitems',null=True,blank=True)
    items=models.ForeignKey(CommonStocksModel, on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
   
    def __str__(self):
        return str(self.credit_note)
    

class CommonTasksModel(CommonBaseModel):
    task=models.CharField(max_length=50,blank=False)
    task_status=models.CharField(max_length=10,choices=task_status,default='incomplete')
  
    taskDay=models.CharField(max_length=10,choices=day,default='Monday')
    assignedto=models.ForeignKey(CommonEmployeesModel,on_delete=models.SET_NULL,blank=True,null=True,related_name="tskempl")
    
    def __str__(self):
    		return self.task

class CommonSalariesModel(CommonBaseModel):
    staff=models.ForeignKey(CommonEmployeesModel,related_name="stafsalrnm",on_delete=models.SET_NULL,null=True,blank=False)
    
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    account=models.ForeignKey(CommonChartofAccountsModel,related_name="amsalrn",on_delete=models.SET_NULL,blank=False,null=True)
    post_status=models.CharField(choices=posting_status, default='waiting', max_length=100,blank=True,null=True)
    
    salary_payable=models.DecimalField(max_digits=30,blank=False,null=False,decimal_places=1,default=0)
   
    mode=models.ForeignKey(CommonPaymentTermsModel, related_name="salripymtn",on_delete=models.SET_NULL,null=True,blank=True)
    currency=models.ForeignKey(CommonCurrenciesModel, related_name="crrnslries",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
    	return str(self.staff)

class CommonJobsModel(CommonBaseModel):
    customer=models.ForeignKey(CommonCustomersModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='jobcustrelname')
   
    job_status=models.CharField(max_length=20, blank=True, null=True,choices=job_status,default="open")
   
    payment_terms=models.ForeignKey(CommonPaymentTermsModel, related_name="jobpymtn",on_delete=models.SET_NULL,null=True,blank=True)
    currency=models.ForeignKey(CommonCurrenciesModel, related_name="crrncjob",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return str(self.number)


class CommonJobItemsModel(CommonBaseModel):
    item=models.ForeignKey(CommonStocksModel, blank=True, null=True, on_delete=models.CASCADE,related_name='itemjobcon')
    quantity=models.FloatField(max_length=20,blank=True,null=True,default=0)
    jobitemconnector= models.ForeignKey(CommonJobsModel, blank=True, null=True, on_delete=models.CASCADE,related_name='itemjobconrelnme')
    def __str__(self):
        return str(self.item)
    

#################################### shipments.... ###############

class CommonTransitModel(CommonBaseModel):
    
    carrier=models.ForeignKey(CommonAssetsModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='carrier_related')
    
    expected=models.DateTimeField(null=True, blank=True)
    transit_status=models.CharField(choices=Shipment_Status,null=True, blank=True, max_length=20,default="Booked")
    origin=models.CharField(null=True, blank=True, max_length=20)
    destination=models.CharField(null=True, blank=True, max_length=20)
    via=models.CharField(choices=Transport_Mode,null=True, blank=True, max_length=20,default="Road")
    
    exit_warehouse=models.ForeignKey(CommonSpacesModel,blank=True,null=True, on_delete=models.CASCADE, related_name='exits')
    entry_warehouse=models.ForeignKey(CommonSpacesModel,blank=True,null=True, on_delete=models.CASCADE, related_name='entries')
    
    dispatched_by=models.ForeignKey(CommonEmployeesModel,related_name='shipment_dispatched_by', on_delete=models.SET_NULL, null=True, blank=True)
    customer=models.ForeignKey(CommonCustomersModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='goods_received')
   
    received_on=models.DateTimeField(blank=True,null=True)
    received_by=models.ForeignKey(CommonEmployeesModel,related_name='shipment_received_by_emplye', on_delete=models.SET_NULL, null=True, blank=True)
    supplier=models.ForeignKey(CommonSuppliersModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='goods_supplied') # Assuming suppliers are customers
   
    delivery_confirmed_by_customer=models.ForeignKey(CommonCustomersModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_deliveries_customer')
    delivery_confirmed_by_employee=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_deliveries_employee')
    delivery_confirmation_date_time=models.DateTimeField(blank=True,null=True)
    delivery_notes=models.CharField(blank=True, null=True,max_length=250)
  
    def __str__(self):
         return '{}'.format(self.number)
 
class CommonTransitItemsModel(CommonBaseModel):
    """
    Individual items within a shipment, linked to CommonStocksModel.....
    """
    
    shipment=models.ForeignKey(CommonTransitModel,blank=True,null=True, on_delete=models.CASCADE, related_name='items')
    items=models.ForeignKey(CommonStocksModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipment_occurrences')
    
    unit_of_measure=models.ForeignKey(CommonUnitsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='items_units_shipment')
    expected=models.DateTimeField(null=True, blank=True)
    expires=models.DateTimeField(null=True, blank=True)
    delivered_on=models.DateTimeField(null=True, blank=True)
    consigner= models.ForeignKey(CommonCustomersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='consignerrelated')
    consignee= models.ForeignKey(CommonCustomersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='consigneerelated')
   
    weight=models.CharField(null=True, blank=True, max_length=50)
    
    length=models.CharField(null=True, blank=True, max_length=50)
    width=models.CharField(null=True, blank=True, max_length=50)
    height=models.CharField(null=True, blank=True, max_length=50)
    received= models.DateTimeField(null=True, blank=True)
    value=models.CharField(blank=True,null=True,max_length=50)
    rate=models.CharField(blank=True,null=True,max_length=50)
   
    shipment_status=models.CharField(choices=Shipment_Status,null=True, blank=True, max_length=20,default="Booked")
    origin= models.CharField(null=True, blank=True, max_length=50)
    destination= models.CharField(null=True, blank=True, max_length=50)
 
    dispatched_by=models.ForeignKey(CommonEmployeesModel,related_name='shipment_dispatched_by_shipment_items', on_delete=models.SET_NULL, null=True, blank=True)
   
    def __str__(self):
        return str(self.items)
     

 ##################33 contacts from the website ############3       
class CommonContactsModel(models.Model):
    name=models.CharField(max_length=50,blank=False,null=True,default="name")
    subject=models.CharField(max_length=50,blank=False,null=True,default="subject")
    email=models.EmailField(max_length=50,blank=False,null=True,default="email")
    message=models.CharField(max_length=255,blank=False,null=True,default="message")
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return str(self.subject)
    



















################################the models below are all fully implemented....look for common areas whwere they can be used in future....#####################################################

class CommonAssetCategoriesModel(CommonBaseModel):
   
    def __str__(self):
        return str(self.description)

class CommonProgramsModel(CommonBaseModel):# not used...may be deleted
    """
    Defines programs that are offered by a particular entity
    for example:
    Sales...sales, manufacturing, repairs, services contracts etc.
    Education...Bachelor of Science in IT, Diploma in Nursing, PhD in MBA etc.
    Healthcare...General surgery, Maternity, Dental, Checkups etc.
    Hospitality...Accommodation, outdoor catering, spacing letting(malls/apartments),conferences, events etc
    Logistics....travelling, tourism, Hajj,Umrah,Cargo, handling, clearing etc
    Realestate...spacing letting(malls/apartments),property management,property development etc
    Services...consultancy, financial services, audit, legal, accounting etc..
    
    """
    
    def __str__(self):
        return str(self.name)

class CommonServicesModel(CommonBaseModel):# not used for now...may be deleted later
    
   
    """
    Defines individual courses/subjects/services/goods within a program that are offered by a particular entity
    for example:
    Sales...selling of various items, item repairs, consultancy etc
    Education...sciences, math, electrical current, strenghth of materials, dental surgery etc..
    Healthcare...general consultations, dental washing, maternity and delivery, heart surgery etc.
    Hospitality...Accommodation, outdoor catering, room bookings,conferences, events etc
    Logistics....ticketing, cargo shipment, cargo handling
    Realestate...letting spaces, building management, BMS
    Services...consultancy, financial services, auditing, legal services, accounting services etc..
    
    
    """
    
    program=models.ForeignKey(CommonProgramsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='coursesprograms')
   
    credits=models.DecimalField(max_digits=4,blank=True,null=True, decimal_places=2, default=0.00, help_text="Credit hours for the course")
   
    is_current=models.CharField(choices=operation_year_options,max_length=50,blank=True,null=True,default="Current")
   
    unitprice=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    quantity=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    unitcost=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    
    normal_range_info=models.CharField(max_length=250, blank=True, null=True,help_text="General normal range information for this test (e.g., '70-110 mg/dL').")
    unit_of_measure=models.CharField(max_length=50, blank=True, null=True,help_text="Standard unit of measure for the test result (e.g., 'mg/dL', 'cells/mm3').")
    unit_of_measure=models.ForeignKey(CommonUnitsModel,related_name="unit_of_measure_services",on_delete=models.SET_NULL,null=True,blank=True)
    
  
    def __str__(self):
        return f"{self.name} ({self.code})"
    