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
    class Meta:
        # ensures that the same value is not repeated in the same company
        unique_together = ('branch', 'division','company')

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
    class Meta:
        # ensures that the same value is not repeated in the same company
        unique_together = ('company', 'division','branch')
    def __str__(self):
        return str(self.department)
    
    def save(self, *args, **kwargs):
        if self.departmentuid is None:
            self.departmentuid=str(uuid4()).split('-')[4]
            self.departmentslug=slugify('{} {}'.format(self.legalname, self.departmentuid))
        self.departmentslug=slugify('{} {}'.format(self.legalname, self.departmentuid))#this is what generates the slug
        self.updatedon=timezone.localtime(timezone.now())
        super(CommonDepartmentsModel, self).save(*args, **kwargs)

# this database serves all types of employees for various industries like doctors, teachers, sales people, etc. 
class CommonCompanyScopeModel(models.Model):# this is the company  hospitality logistics
    name=models.CharField(max_length=30,blank=False,null=False,unique=False,default="Your Scope")
    comments=models.CharField(max_length=30,blank=False,null=False,unique=False,default="scope comments")
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name="usrcmpscop")
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="compscopesconn",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvscpe",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="scopebrcnh",on_delete=models.SET_NULL,null=True,blank=True)
    department= models.ForeignKey(CommonDepartmentsModel,related_name="scopdptm",on_delete=models.SET_NULL,null=True,blank=True)
  
    def __str__(self):
        return self.name
    
class CommonTaxParametersModel(models.Model):
    taxname=models.CharField(null=True, blank=True, max_length=30,unique=False)
    taxdescription= models.CharField(null=True, blank=True, max_length=30)
    taxtype=models.CharField(choices=taxoptions, blank=True, max_length=30)
    taxrate=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    owner=models.ForeignKey(User, related_name="cmnowntax",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmntaxcmp",on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvstxprm",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="txpbrcnh",on_delete=models.SET_NULL,null=True,blank=True)
    department= models.ForeignKey(CommonDepartmentsModel,related_name="txprdptm",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return str(self.taxname)
        #return self.taxname +"   "+str(self.taxrate)+str('%')
    def clean(self):
        if self.taxrate<0:
            raise ValidationError("Tax Rate cannot be negative")

class CommonSupplierTaxParametersModel(models.Model):
    taxname=models.CharField(null=True, blank=True, max_length=30,unique=False)
    taxdescription= models.CharField(null=True, blank=True, max_length=30)
    taxtype=models.CharField(choices=taxoptions, blank=True, max_length=30)
    taxrate=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    owner=models.ForeignKey(User, related_name="supplrcmnowntax",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="supplrcmntaxcmp",on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="supplirdvstxprm",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="supplirtxpbrcnh",on_delete=models.SET_NULL,null=True,blank=True)
    department= models.ForeignKey(CommonDepartmentsModel,related_name="supplirtxprdptm",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return str(self.taxname)
        #return self.taxname +"   "+str(self.taxrate)+str('%')
    def clean(self):
        if self.taxrate<0:
            raise ValidationError("Tax Rate cannot be negative")
        
class CommonCurrenciesModel(models.Model):
    description=models.CharField(max_length=30,blank=False,null=True,unique=False)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="owncrrncy",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpcrrncy",on_delete=models.CASCADE,null=True,blank=True)
    comments=models.CharField(null=True, blank=False, max_length=30)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvscrrncy",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="currnybrnch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="currncydpt",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return str(self.description)


class CommonPaymentTermsModel(models.Model):
    description=models.CharField(max_length=50,blank=False,null=True,unique=False)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="owpymnterms",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmppymntrms",on_delete=models.CASCADE,null=True,blank=True)
    comments=models.CharField(null=True, blank=False, max_length=50)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvspymtrm",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchpymntrms",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="paymntrmsdpt",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return str(self.description)
    
class CommonUnitsModel(models.Model):
    description=models.CharField(max_length=50,blank=False,null=True,unique=False)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="owner_units",blank=True,null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmppy_units",on_delete=models.CASCADE,null=True,blank=True)
    comments=models.CharField(null=True, blank=False, max_length=50)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_units",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_units",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="paym_units",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return str(self.description)

class CommonOperationYearsModel(models.Model):
    """
    defines the opreational/fiscal/academic year..
    
    """
    year=models.CharField(max_length=50,blank=True,default="Operation Year",null=True,unique=False,help_text="e.g., 2023-2024")
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="owner_operation_year",blank=True,null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmppy_operation_year",on_delete=models.CASCADE,null=True,blank=True)
    comments=models.CharField(null=True, blank=True, max_length=50)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_operation_year",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_operation_year",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="paym_operations_year",on_delete=models.SET_NULL,null=True,blank=True)
    
    start_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    end_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    is_current=models.CharField(choices=operation_year_options,max_length=50,blank=True,null=True,default="Current")
  
    def __str__(self):
        return str(self.year)
    
class CommonOperationYearTermsModel(models.Model):
    """
    this model captures operational year sections like terms, semisters, quarters ...etc
    """
    name=models.CharField(max_length=100, help_text="e.g., Term 1, Semester A",blank=True,null=True)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="owner_operation_year_terms",blank=True,null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmppy_operation_year_terms",on_delete=models.CASCADE,null=True,blank=True)
    comments=models.CharField(blank=True,null=True, max_length=50)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_operation_year_term",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_operation_year_terms",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="paym_operation_year_term",on_delete=models.SET_NULL,null=True,blank=True)
    
    is_current=models.CharField(choices=operation_year_options,max_length=50,blank=True,null=True,default="Current")
   
    operation_year=models.ForeignKey(CommonOperationYearsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='termsyear')
    start_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    end_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    is_active=models.BooleanField(default=False,blank=True,null=True)
   
    def __str__(self):
        return str(self.name)


#########################################3 stock, items, services, subjects categories.. ##############################################
class CommonCategoriesModel(models.Model):
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
   
    description=models.CharField(max_length=30, blank=False, null=True)
    owner=models.ForeignKey(User, related_name="cmnurstkcat",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmnstcatrln",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsstockcats",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchstockcats",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptstockcats",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    comments=models.CharField(null=True, blank=True, max_length=50)
    
    name=models.CharField(max_length=255,blank=True,null=True)
    code=models.CharField(max_length=50,blank=True,null=True, unique=False, help_text="Unique code for the program, e.g., BSCIT")
    
    operation_year=models.ForeignKey(CommonOperationYearsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='categories_operation_year')
    operation_term=models.ForeignKey(CommonOperationYearTermsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='terms_categories')
    is_current=models.CharField(choices=operation_year_options,max_length=50,blank=True,null=True,default="Current")
   
    start_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    end_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    def __str__(self):
    		return str(self.name) # this will show up in the admin area

###################3 comon codes ##############
class CommonCodesModel(models.Model):
    """
    this defines the codes used by various entities.....
    sales...codes of various items...
    healthcare...codes of various places, items, staff, wards, rooms, equipment etc
    logistics...codes of airports, cities, items, passengers etc..
    realestates...codes of properties, places, items, equipment etc
    education... codes of places, items, machines, equipment, student registeration numbers etc.
    
    """
    owner=models.ForeignKey(User,related_name="common_codes_owners",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="acommon_codes_company_relname",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="common_codes_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="common_codes_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="common_codes_department",on_delete=models.SET_NULL,null=True,blank=True)
    code=models.CharField(max_length=100,blank=True,null=True)
    name=models.CharField(max_length=100,blank=True,null=True)
    description=models.CharField(max_length=50,blank=True,null=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    class Meta:
        # ensures that the same value is not repeated in the same company
        unique_together = ('company', 'code','name')
    
    def __str__(self):
        return f"{self.code}: {self.name}:"



# #################3 HRM ################    
class CommonEmployeesModel(models.Model):
    staffNo=models.CharField(max_length=50,blank=True,null=True)
    firstName=models.CharField(max_length=50,blank=False,null=True)
    lastName=models.CharField(max_length=50,blank=True,null=True)
    middleName=models.CharField(max_length=50,blank=True,null=True)
    gender=models.CharField(max_length=25, blank=True, null=True,choices=gender)
    title=models.CharField(max_length=50,blank=True,null=True)
    education=models.CharField(max_length=50,blank=True,null=True)
    comment=models.CharField(max_length=50,blank=True,null=True)
    dateJoined =  models.DateTimeField(auto_now_add=True,blank=True,null=True)
    salary=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    total_salary_paid=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    salary_payable=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    salary_balance=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    username=models.OneToOneField(User, on_delete=models.CASCADE,related_name="secrlmmemply",null=True)
    uniqueId=models.CharField(null=True, blank=True, max_length=150)
    sysperms=models.CharField(choices=rights, blank=True, null=True,max_length=30,default="staff")
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="emplcomprlnmefsammnapp",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="emplydvs",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="emplybrnch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="emplydpt",on_delete=models.SET_NULL,null=True,blank=True)
    stffslug=models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.firstName)
        
    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId=str(uuid4()).split('-')[4]
            self.stffslug=slugify('{} {} {} {} {}'.format(self.company,self.company.address, self.uniqueId,self.firstName,self.middleName))
        self.stffslug=slugify('{} {} {} {} {}'.format(self.company,self.company.address, self.uniqueId,self.firstName,self.middleName))#this is what generates the slug
        super(CommonEmployeesModel, self).save(*args, **kwargs)

class CommonApproversModel(models.Model):
    company=models.ForeignKey(CommonCompanyDetailsModel, on_delete=models.CASCADE, related_name='approver_groups')
    comments=models.CharField(max_length=100,null=True,blank=True)
    approvers=models.ForeignKey(CommonEmployeesModel,null=True,blank=True, related_name='apprvrusrmbmrs',on_delete=models.SET_NULL) # Users in this group
    division=models.ForeignKey(CommonDivisionsModel,related_name="apprvrdvs",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="apprvrbrnch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="apprvrdept",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    def __str__(self):
        return str(self.approvers)

########################## CHART OF ACCOUNTS ##########################3
class CommonGeneralLedgersModel(models.Model):
    description=models.CharField(max_length=50,blank=False,null=True,unique=False)
    balance=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="usrglrlnm",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="glcmprlnm",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="gldvsrln",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="glbrnchrlnm",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="gldptrlnm",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    def __str__(self):
        return str(self.description)

class CommonChartofAccountsModel(models.Model):
    code=models.IntegerField(blank=True,null=True)
    description=models.CharField(max_length=50,blank=True,null=True)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="usrchacrln",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpchaccrlnm",on_delete=models.SET_NULL,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="chaccdvsrln",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="chaccbrnchrlnm",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="chaccdptrlnm",on_delete=models.SET_NULL,null=True,blank=True)
    balance=models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=True,default=0.00)
    category=models.ForeignKey(CommonGeneralLedgersModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='chaccmrln')
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    comments=models.CharField(max_length=100,blank=True,null=True,default="Comments")
    statement=models.CharField(choices=chart_of_account_statement_type,max_length=20,blank=True,null=True)
    def __str__(self):
        return str(self.description)

########################## banks #########################
class CommonBanksModel(models.Model):
    name=models.CharField(max_length=50,blank=False,null=True)
    account=models.CharField(max_length=30,blank=True,null=True)
    balance=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    deposit=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    withdrawal=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    comments=models.CharField(max_length=100,blank=True,null=True, default='comment')
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="usrbnkrlnm",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpbnkrlnm",on_delete=models.SET_NULL,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsbnk",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchbnk",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="bnkdptmn",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    def __str__(self):
        return '{}'.format(self.name)

############################ SHAREHOLDER DEPOSITS AND INVESTMENTS #####################################3
class CommonShareholderBankDepositsModel(models.Model):
    description=models.CharField(max_length=50,blank=True,null=True)
    bank=models.ForeignKey(CommonBanksModel,related_name="depositbankrelnefds",on_delete=models.SET_NULL,blank=False,null=True)
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    comments=models.CharField(max_length=30,blank=True,null=True, default='Deposit comments')
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="usrbnksrlnmedf",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="depocmprlnmfd",on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    equity=models.ForeignKey(CommonChartofAccountsModel,related_name="dpscustrlnmdfd",on_delete=models.SET_NULL,blank=False,null=True)
    asset=models.ForeignKey(CommonChartofAccountsModel, blank=True,null=True,on_delete=models.SET_NULL,related_name='coabnkdpasset')
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsbnkdpst",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchbnkdpst",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="bnkdptmndpst",on_delete=models.SET_NULL,null=True,blank=True)
    status=models.CharField(choices=posting_status, default='waiting', max_length=20,blank=True,null=True)
    def __str__(self):
        return '{}'.format(self.description)

######################3 WITHDRAWALS ############33
class CommonBankWithdrawalsModel(models.Model):
    description=models.CharField(max_length=50,blank=True,null=True)
    bank=models.ForeignKey(CommonBanksModel,related_name="wthdrbnkrelnm",on_delete=models.SET_NULL,blank=False,null=True)
    amount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    comments=models.CharField(max_length=30,blank=True,null=True, default='Withdrawal')
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="withdrusrbnkrlnmes",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="withcmprlnm",on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    asset=models.ForeignKey(CommonChartofAccountsModel, blank=False,null=True,on_delete=models.SET_NULL,related_name='coabnka')
    bankcoa=models.ForeignKey(CommonChartofAccountsModel, blank=False,null=True,on_delete=models.SET_NULL,related_name='coabnkafrm')
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsbnkwithdrwl",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchbnkwithdrwl",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="bnkdptmnwithdrwl",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return '{}'.format(self.description)


########################## Emails and SMSs #########################
class CommonEmailsModel(models.Model):
    subject=models.CharField(max_length=255,blank=True,null=True)
    message=models.CharField(max_length=255,blank=True,null=True)
    sender=models.EmailField(max_length=50,blank=True,null=True, default='sender')
    recipient=models.EmailField(max_length=50,blank=True,null=True, default='recipients')
    sender=models.CharField(max_length=50,blank=True,null=True, default='comment')
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="emlrlnm",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="emailrlnm",on_delete=models.SET_NULL,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsemil",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchemil",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="emaildptmn",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
   
    def __str__(self):
        return '{}'.format(self.subject)


#################3 suppliers ################
class CommonSuppliersModel(models.Model):
    name=models.CharField(null=True, blank=False, max_length=30)
    phone=models.CharField(null=True, blank=True, max_length=30)
    email=models.EmailField(null=True, blank=True, max_length=30)
    city=models.CharField(null=True, blank=True, max_length=30)
    address=models.CharField(null=True, blank=True, max_length=30)
    balance=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    turnover=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    contact=models.CharField(null=True, blank=True, max_length=30)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="spplusowncrln",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="suppusrlnm",on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    comments=models.CharField(null=True, blank=True, max_length=50)
    country=models.CharField(null=True, blank=True, max_length=50)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsspplr",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchsupplr",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptsppl",on_delete=models.SET_NULL,null=True,blank=True)
    
    coverage=models.TextField(max_length=250,blank=True,null=True,default='Insurance')
  
    is_active=models.BooleanField(default=True,blank=True,null=True)
    
   
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return '{}'.format(self.name)
    
class CommonSupplierPaymentsModel(models.Model):
    supplier=models.ForeignKey(CommonSuppliersModel,related_name="allifsuprln",on_delete=models.SET_NULL,blank=True,null=True)
    amount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=100,blank=True,null=True, default='Supplier Payment')
    description=models.CharField(max_length=50,blank=True,null=True, default='Supplier payment')
    account=models.ForeignKey(CommonChartofAccountsModel,related_name="amesupayrlnm",on_delete=models.SET_NULL,blank=True,null=True)
    mode=models.ForeignKey(CommonPaymentTermsModel, related_name="supplrpymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    status=models.CharField(choices=posting_status, default='waiting', max_length=100,blank=True,null=True)
    owner=models.ForeignKey(User, related_name="supymnt",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpsupym",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsspplpymnt",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchspplpymnt",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptspplpymnt",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return '{}'.format(self.supplier)

class CommonSupplierStatementsModel(models.Model):
    supplier=models.ForeignKey(CommonSuppliersModel,related_name="supstmrl",on_delete=models.CASCADE,blank=True,null=True)
    debit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    credit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    balance=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=30,blank=True,null=True, default='comment')
    owner=models.ForeignKey(User, related_name="ownspstmnt",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpsplst",on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return '{}'.format(self.supplier)
    
#.... customers .... this include normal customers, students, etc
class CommonCustomersModel(models.Model):
    uid=models.CharField(null=True, blank=True, max_length=100,unique=True)
    name=models.CharField(null=True, blank=False, max_length=50)#customer, student, patient---can be entity/person
    phone=models.CharField(null=True, blank=True, max_length=30)
    email=models.EmailField(null=True, blank=True, max_length=50)
    city=models.CharField(null=True, blank=True, max_length=30)
    address=models.CharField(null=True, blank=True, max_length=30)
    sales=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    balance=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    turnover=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    contact=models.CharField(null=True, blank=True, max_length=30)
    uniqueId=models.CharField(null=True, blank=True, max_length=100)
    customerslug=models.SlugField(max_length=50, unique=True, blank=True, null=True)
    owner=models.ForeignKey(User,related_name="cmnusrcstmrln",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmncmprnm",on_delete=models.CASCADE,null=True,blank=True)
    fullName=models.CharField(null=True, blank=False, max_length=20)# this is for slug creation
    

    paymentType=models.ForeignKey(CommonPaymentTermsModel, related_name="custmerrpymntrms",on_delete=models.SET_NULL,null=True,blank=True)
    #..... end.... below fields is special for healthcare entities setup....

    #..... start.... below fields is special for educational setup....
    #form=models.ForeignKey(CommonFormsModel,on_delete=models.SET_NULL,blank=True,null=True)
    #className=models.ForeignKey(CommonClassesModel,on_delete=models.SET_NULL,blank=True,null=True)
    course_category=models.ForeignKey(CommonCategoriesModel,blank=True,null=True, on_delete=models.CASCADE, related_name='course_enrollments')
    operation_year=models.ForeignKey(CommonOperationYearsModel, on_delete=models.CASCADE, related_name='year_enrollments',null=True,blank=True)
    term=models.ForeignKey(CommonOperationYearTermsModel, on_delete=models.CASCADE, related_name='term_enrollments',blank=True,null=True)
    enrollment_date=models.DateField(auto_now_add=True,blank=True,null=True)
    status=models.CharField(max_length=4, choices=student_status_choices, default='ENR',blank=True,null=True)

     #..... end.... below fields is special for educational setup....
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    comments=models.CharField(null=True, blank=True, max_length=50)
    country=models.CharField(null=True, blank=True, max_length=50)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvscustmrs",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchcustmrs",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptcustmrs",on_delete=models.SET_NULL,null=True,blank=True)
    

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
   
class CommonCustomerPaymentsModel(models.Model):
    customer=models.ForeignKey(CommonCustomersModel,related_name="allifcustpaymentreltedname",on_delete=models.CASCADE,blank=True,null=True)
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=50,blank=True,null=True, default='comment')
    account=models.ForeignKey(CommonChartofAccountsModel,related_name="allifcustpymaccrelnm",on_delete=models.SET_NULL,blank=True,null=True)
    mode=models.ForeignKey(CommonPaymentTermsModel, related_name="custmrpymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    status=models.CharField(choices=posting_status, default='waiting', max_length=200,blank=True,null=True)
    owner=models.ForeignKey(User, related_name="ownrcstmpymnt",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpcspymnt",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvscustmrpymnt",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchcustpymnt",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptcustpymnt",on_delete=models.SET_NULL,null=True,blank=True)
    description=models.CharField(max_length=50,blank=True,null=True, default='Customer payment')
    
    def __str__(self):
        return '{}'.format(self.customer)

class CommonCustomerStatementsModel(models.Model):
    customer=models.ForeignKey(CommonCustomersModel,related_name="custstmrlnm",on_delete=models.CASCADE,blank=True,null=True)
    debit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    credit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    balance=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=30,blank=True,null=True, default='comment')
    owner=models.ForeignKey(User, related_name="usrcuststmnrln",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpcstsmnreln",on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return '{}'.format(self.customer)

class CommonLedgerEntriesModel(models.Model): # this is the journal entries...
    supplier=models.ForeignKey(CommonSuppliersModel,related_name="sppldgentr",on_delete=models.CASCADE,blank=True,null=True)
    customer=models.ForeignKey(CommonCustomersModel,related_name="cstmldgentr",on_delete=models.CASCADE,blank=True,null=True)
    staff=models.ForeignKey(CommonEmployeesModel,related_name="empldgentr",on_delete=models.CASCADE,blank=True,null=True)
    debit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    credit=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    originalamount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    newamount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    balance=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=30,blank=True,null=True, default='comments')
    owner=models.ForeignKey(User, related_name="usrldgentr",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpyldgentr",on_delete=models.CASCADE,null=True,blank=True)
    ledgowner=models.CharField(choices=ledgerentryowner, max_length=50,blank=True,default="staff")
   
    def __str__(self):
        return '{}'.format(self.comments)
 

class CommonAssetsModel(models.Model):
    """
    thi can represent a normal asset to any company...vehicles, equipment, properties etc...
    
    The asset can be a building/property for the entity... for instance in:
    sales... building that the company may own or reside in
    healthcare...this is the hospital building that contains the wards and other sections of operation
    realestate...these are the properties/buildings of the company...like appartments etc.
    education... this represents dormitaries or other buildings of the school
    logistics and other sectors....building owned/managed by the company
    """
    owner=models.ForeignKey(User, related_name="cmnassetown",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmncmpassetrln",on_delete=models.CASCADE,null=True,blank=True)
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
    status=models.CharField(choices=posting_status, default='waiting',max_length=20,blank=True,null=True)
    asset_status=models.CharField(choices=asset_current_status,max_length=20,blank=True,null=True)
    depreciation=models.CharField(choices=depreciation_method,max_length=50,blank=True,null=True)
    depreciated_by=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    comments=models.CharField(null=True, blank=True, max_length=50)
    category=models.ForeignKey(CommonCategoriesModel, related_name="assetcat",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, blank=True, null=True,on_delete=models.SET_NULL,related_name='asstdprmtn')
    employee_in_charge=models.ForeignKey(CommonEmployeesModel, blank=True, null=True,on_delete=models.SET_NULL,related_name='asstemply')
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsassts",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchassts",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptassts",on_delete=models.SET_NULL,null=True,blank=True)
    
    
    maker_name=models.CharField(max_length=50, blank=True, null=True)
    equipment_model=models.CharField(max_length=50, blank=True, null=True)
    manufactured_year=models.CharField(max_length=30, blank=True, null=True)
    equipment_status=models.CharField(max_length=50, blank=True, null=True,choices=equipment_status_options)
   
    starting_odometer=models.CharField(default=0,blank=True,null=True,max_length=250)
    primary_meter=models.CharField(max_length=30, blank=True, null=True,choices=primary_meter_options,default='Kilometers')
    
    oil_type=models.CharField(max_length=30, blank=True, null=True,choices=oil_options)
    oil_capacity=models.CharField(blank=True,null=True,max_length=30)
   
    energy_usage= models.CharField(null=True, blank=True,default=0,max_length=250)
    comments=models.CharField(blank=True,null=True,max_length=30)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    
    plate_number=models.CharField(max_length=50, unique=False,null=True,blank=True)
   
    capacity_kg=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Carrying capacity in kilograms")
  
    last_service_date=models.DateField(blank=True, null=True)
    next_service_due=models.DateField(blank=True, null=True)
    is_active=models.BooleanField(default=True)

    
    def __str__(self):
        return str(self.description)
    @property
    def asset_total_amount(self):
        assetamount=self.quantity*self.value
        return assetamount

#########################################3 SPACES ##############################################

class CommonSpacesModel(models.Model):
    """
    It represents any definable, usable, and often bookable/assignable unit or area within a building or property.
    This can be a hotel room, halls, a hospital wards, a classrooms, an office, an apartment, a restaurant table, an event hall, a storage bay etc.
    """
    owner=models.ForeignKey(User, related_name="owned_rooms", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_rooms", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_rooms", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_rooms", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_rooms", on_delete=models.SET_NULL, null=True, blank=True)
    
    asset=models.ForeignKey(CommonAssetsModel, related_name="asset_space", on_delete=models.SET_NULL, null=True, blank=True)
    space_number=models.CharField(max_length=50,blank=True,null=True)
    number_of_units=models.CharField(max_length=50,blank=True,null=True)
    name=models.CharField(max_length=30,blank=True,null=True)
    description=models.CharField(max_length=100,blank=True,null=True)
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
    
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
   
    def __str__(self):
        return str(self.name)


class CommonSpaceUnitsModel(models.Model):
    """
    this defines the sub-units of available spaces....
    sales... office rooms, cubicles, etc
    healthcare...rooms, beds, etc
    education...rooms, beds, etc
    realestates...rooms,beds, etc
    
    """
    owner=models.ForeignKey(User, related_name="owned_space_units", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_space_units", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_space_units", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_space_units", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_space_units", on_delete=models.SET_NULL, null=True, blank=True)
    
    space=models.ForeignKey(CommonSpacesModel, related_name="units_space", on_delete=models.SET_NULL, null=True, blank=True)
    space_number=models.CharField(max_length=250,blank=True,null=True)
    name=models.CharField(max_length=50,blank=True,null=True)
    description=models.CharField(max_length=250,blank=True,null=True)
    space_type=models.CharField(max_length=250,blank=True,null=True, choices=PROPERTY_TYPES, default='AVAIL')
    space_floor=models.PositiveSmallIntegerField(choices=FLOOR_CHOICES, blank=True, null=True)
    
    current_status = models.CharField(max_length=250,blank=True,null=True, choices=CURRENT_STATUS_CHOICES, default='AVAIL')
    date=models.DateField(blank=True,null=True,auto_now_add=True)
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
class CommonExpensesModel(models.Model):
    owner=models.ForeignKey(User, related_name="cmnurexpns",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmnexpcmpn",on_delete=models.CASCADE,null=True,blank=True)
    #funding_account=models.ForeignKey(CommonChartofAccountsModel, blank=False,null=True,on_delete=models.SET_NULL,related_name='coaexprelnanemconcmm')
    expense_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True, on_delete=models.SET_NULL,related_name='coaexprelnamepaytocmm')
    supplier=models.ForeignKey(CommonSuppliersModel, blank=False, null=True, on_delete=models.SET_NULL,related_name='expsupprelanmeconcmm')
    mode=models.ForeignKey(CommonPaymentTermsModel, related_name="expnspymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    description=models.CharField(max_length=50,blank=False,null=True)
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    comments=models.CharField(max_length=30,blank=True,null=True)
    status=models.CharField(choices=posting_status, default='waiting', max_length=20,blank=True,null=True)
    #quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    #equity_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True, on_delete=models.SET_NULL,related_name='coexprln')
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsexpns",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchexpns",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptexpns",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return str(self.description)
   
class CommonStocksModel(models.Model):
    
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
    partNumber=models.CharField(max_length=30, blank=False, null=False)# unique prevents data duplication
    description=models.CharField(max_length=50, blank=False, null=False)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    buyingPrice=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    unitcost=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    standardUnitCost=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    unitPrice=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    comments=models.CharField(null=True, blank=True, max_length=100)
    criticalnumber=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    inventory_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='coainvrelnm')
    income_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='coaincomerelnm')
    expense_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='coaexprelnm')
    owner=models.ForeignKey(User, related_name="cmnurstkrln",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmnestkmpn",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsstocks",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchstocks",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptstocks",on_delete=models.SET_NULL,null=True,blank=True)
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
        unique_together = ('company', 'partNumber', 'warehouse')
        
    def __str__(self):
    		return str(self.description) # this will show up in the admin area

class CommonSpaceItemsModel(models.Model):
    space=models.ForeignKey(CommonSpacesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='wrhseitms')
    items=models.ForeignKey(CommonStocksModel,blank=False,null=False, on_delete=models.CASCADE,related_name='wrhseitemsstck')
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    class Meta:
        # THIS IS THE CRUCIAL ADDITION/CONFIRMATION
        unique_together = ('items', 'space')
    def __str__(self) :
        return str(self.items)

#########################################3 STOCK ##############################################
class CommonStockTransferOrdersModel(models.Model):
    number=models.CharField(max_length=50, blank=False, null=True)
    owner=models.ForeignKey(User, related_name="intcmpstcktrnsfrsown",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpnintcmpstcktrnsfrs",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsintcmpstcktrnsfrs",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchintcmpstcktrnsfrs",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptintcmpstcktrnsfrs",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    comments=models.CharField(null=True, blank=True, max_length=50)
    status=models.CharField(choices=posting_status, default='waiting', max_length=20)
 
    from_store=models.ForeignKey(CommonSpacesModel,related_name="frmintcmpstcktrnsfrs",on_delete=models.SET_NULL,null=True,blank=True)
    to_store=models.ForeignKey(CommonSpacesModel,related_name="tointcmpstcktrnsfrs",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
    		return str(self.number) # this will show up in the admin area

class CommonStockTransferOrderItemsModel(models.Model):
    items=models.ForeignKey(CommonStocksModel,related_name="stcktrnsfordrlns",on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    comments=models.CharField(null=True, blank=True, max_length=50)
    trans_ord_items_con=models.ForeignKey(CommonStockTransferOrdersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='poitrelname')
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def __str__(self):
        return '{}'.format(self.items)
    #below calculates the total selling price for the model


################# TRANSACTIONS SECTION ############3

class CommonTransactionsModel(models.Model):# very important model
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
    trans_number=models.CharField(max_length=50, blank=True, null=True)
    employee_in_charge=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="encounters_as_primary_doctor",help_text="The main employee attending this encounter.")
    customer=models.ForeignKey(CommonCustomersModel, on_delete=models.SET_NULL,blank=True,null=True, related_name="custmtransrlnme",help_text="The customer associated with this encounter.")
    owner=models.ForeignKey(User, related_name="owned_encounters", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_encounters", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_encounters", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_encounters", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_encounters", on_delete=models.SET_NULL, null=True, blank=True)
    
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(blank=True,null=True)
    description=models.CharField(max_length=255,blank=True,null=True)
    comments=models.CharField(max_length=255,blank=True,null=True)
    name=models.CharField(max_length=255,blank=True,null=True)
    code=models.CharField(max_length=50,blank=True,null=True, unique=False, help_text="Unique code for the program, e.g., BSCIT")
    operation_year=models.ForeignKey(CommonOperationYearsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='common_orders_operation_year')
    operation_term=models.ForeignKey(CommonOperationYearTermsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='terms_common_orders')
    payment_mode=models.ForeignKey(CommonPaymentTermsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='terms_payment_mode_trans')
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    def __str__(self):
        return str(self.customer)

class CommonTransactionItemsModel(models.Model):
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
    comments=models.CharField(blank=True, null=True,help_text="general comments",max_length=30)
    date=models.DateField(blank=True,null=True)
    owner=models.ForeignKey(User, related_name="ownr_assessmente",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpassessment",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsassessment",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchassessment",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptassessment",on_delete=models.SET_NULL,null=True,blank=True)
    description=models.CharField(blank=True, null=True,help_text="Descriptions.",max_length=30)
    def __str__(self):
        return str(self.items)

class CommonSpaceBookingItemsModel(models.Model):
    
    
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
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return str(self.space_unit)
    @property
    def space_allocation_amount(self):
        booking_amount=self.quantity * self.space_unit.unitprice
        return booking_amount


class CommonProgressModel(models.Model):
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
    
    owner=models.ForeignKey(User, related_name="ownvtlsgns",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpvtlsgns",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsvtlsgns",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchvtlsgns",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptvtlsgns",on_delete=models.SET_NULL,null=True,blank=True)
    description=models.CharField(max_length=250, blank=True, null=True)
   
    trans_number=models.ForeignKey(CommonTransactionsModel, on_delete=models.CASCADE, related_name="vital_signs", blank=True, null=True,help_text="The encounter this vital signs record belongs to.")
    
    date=models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date', auto_now_add
    recorded_on = models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of measurement
   
    def __str__(self):
        return str(self.trans_number.customer)
    

    
################################## PURCHASES ###########3

class CommonPurchaseOrdersModel(models.Model):
    class Status(models.TextChoices): # <--- Define choices using TextChoices
        DRAFT = 'Draft', 'Draft'
        PENDING_APPROVAL = 'Pending Approval', 'Pending Approval'
        APPROVED = 'Approved', 'Approved'
        ISSUED = 'Issued', 'Issued (GIN Created)'
        RECEIVED = 'Received', 'Received (GRN Created)'
        CANCELLED = 'Cancelled', 'Cancelled'

    owner=models.ForeignKey(User, related_name="cmnownpo",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmncmpnpo",on_delete=models.CASCADE,null=True,blank=True)
    po_number=models.CharField(null=True, blank=True, max_length=100)
    uplift=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=2)
    comments=models.CharField(null=True, blank=True, max_length=100)
    supplier=models.ForeignKey(CommonSuppliersModel,related_name="suplporelnme",on_delete=models.SET_NULL,blank=False,null=True)
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    taxamount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    misccosts=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    grandtotal=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    amounttaxincl=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    posting_po_status=models.CharField(choices=posting_status, default='waiting', max_length=100,blank=True,null=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvspurchases",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchpurchss",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptpurchss",on_delete=models.SET_NULL,null=True,blank=True)
    description=models.CharField(null=True, blank=True, max_length=100)
    payment_terms=models.ForeignKey(CommonPaymentTermsModel, related_name="popymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    delivery=models.CharField(null=True, blank=True, max_length=100)
    currency=models.ForeignKey(CommonCurrenciesModel, related_name="crrncypo",on_delete=models.SET_NULL,null=True,blank=True)
    taxrate=models.ForeignKey(CommonSupplierTaxParametersModel,related_name="sppltxrt",on_delete=models.SET_NULL,blank=True,null=True)
    approval_status= models.CharField(max_length=50, choices=Status.choices, default=Status.DRAFT) 
    def __str__(self):
        return str(self.po_number)

class CommonPurchaseOrderItemsModel(models.Model):
    items=models.ForeignKey(CommonStocksModel,related_name="poitemrallirelnm",on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    unitcost=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    po_item_con= models.ForeignKey(CommonPurchaseOrdersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='poitrelname')
    taxRate=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    discount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,default=0)
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
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
    

class CommonPurchaseOrderMiscCostsModel(models.Model):
    supplier=models.ForeignKey(CommonSuppliersModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='suppmiscrlnme')
    description=models.CharField(max_length=50, blank=True, null=True)
    unitcost=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    po_misc_cost_con= models.ForeignKey(CommonPurchaseOrdersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='pomiscrlnm')
    date= models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return '{}'.format(self.description)
    @property
    def purchase_order_misc_cost(self):
        po_misc_cost=self.quantity * self.unitcost
        return po_misc_cost


################################3 QUOTES ###########################3
class CommonQuotesModel(models.Model):
    number=models.CharField(null=True, blank=True, max_length=20)
    description=models.CharField(blank=True,null=True,default='Quotation',max_length=100)
    customer=models.ForeignKey(CommonCustomersModel,related_name="allifrelatcustquote",on_delete=models.SET_NULL,blank=True,null=True)
    prospect=models.CharField(choices=prospects, default='Default', max_length=20)
    comments=models.CharField(blank=True,null=True,default='Quote',max_length=20)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    total=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    totalwithtax=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    totalwithdiscount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discount=models.CharField(choices=givediscount, default='No', max_length=20)
    tax=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discountValue= models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    salestax=models.ForeignKey(CommonTaxParametersModel,related_name="txqr",on_delete=models.SET_NULL,blank=True,null=True)
    taxAmount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discountAmount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    owner=models.ForeignKey(User, related_name="cmnownqts",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmnqtsmpn",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsqts",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchqts",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptqtess",on_delete=models.SET_NULL,null=True,blank=True)
    grandtotal=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    payment_terms=models.ForeignKey(CommonPaymentTermsModel, related_name="qtesspymntermdd",on_delete=models.SET_NULL,null=True,blank=True)
    delivery=models.CharField(null=True, blank=True, max_length=100)
    currency=models.ForeignKey(CommonCurrenciesModel, related_name="crrncyqtes",on_delete=models.SET_NULL,null=True,blank=True)
   
    def __str__(self):
        return '{}'.format(self.number)
 
class CommonQuoteItemsModel(models.Model):
    description=models.ForeignKey('CommonStocksModel',related_name="allifquoteitemdescrelatednm",on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    allifquoteitemconnector= models.ForeignKey(CommonQuotesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='allifquoteitemrelated')
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return '{}'.format(self.description)
    #below calculates the total selling price for the model
    @property
    def quote_selling_price(self):
        selling_price=self.quantity * self.description.unitPrice
        return selling_price
    @property
    def quote_selling_price_with_discount(self):
        if self.discount!=None:
            selling_price_with_disc=(self.quantity * self.description.unitPrice)*(1-(self.discount/100))
        else:
            selling_price_with_disc=(self.quantity * self.description.unitPrice)
        return selling_price_with_disc
    @property
    def quote_tax_amount(self):
        qtetaxamount=self.quantity* self.description.unitPrice*(1-(self.discount/100))*(self.description.taxrate.taxrate/100)
        return qtetaxamount

########################### INVOICES ################################
class CommonInvoicesModel(models.Model):
    number=models.CharField(null=True, blank=True, max_length=20)
    description=models.CharField(blank=True,null=True,default='Invoice',max_length=100)
    customer=models.ForeignKey(CommonCustomersModel,related_name="allifrelatcustinvce",on_delete=models.SET_NULL,blank=True,null=True)
    status=models.CharField(blank=True,null=True,choices=invoiceStatus, default='Current', max_length=20)
    comments=models.CharField(blank=True,null=True,default='Invoice Comments',max_length=50)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    total=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    totalwithtax=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    totalwithdiscount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discount=models.CharField(choices=givediscount, default='No', max_length=20)
    tax=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discountValue=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    salestax=models.ForeignKey(CommonTaxParametersModel,related_name="txinvce",on_delete=models.SET_NULL,blank=True,null=True)
    taxAmount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discountAmount= models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    owner=models.ForeignKey(User, related_name="cmnowninvcs",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmninvsmpn",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsinvc",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchinvc",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptinvcs",on_delete=models.SET_NULL,null=True,blank=True)
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
 
class CommonInvoiceItemsModel(models.Model):
    description=models.ForeignKey(CommonStocksModel,related_name="invitmstckrlnm",on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    discount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    allifinvitemconnector= models.ForeignKey(CommonInvoicesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='invitmsrelnm')
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return '{}'.format(self.description)
    #below calculates the total selling price for the model
    @property
    def invoice_selling_price(self):
        selling_price=self.quantity * self.description.unitPrice
        return selling_price
    @property
    def invoice_selling_price_with_discount(self):
        if self.discount!=None:
            selling_price_with_disc=(self.quantity * self.description.unitPrice)*(1-(self.discount/100))
        else:
            selling_price_with_disc=(self.quantity * self.description.unitPrice)
        return selling_price_with_disc
    @property
    def invoice_tax_amount(self):
        qtetaxamount=self.quantity* self.description.unitPrice*(1-(self.discount/100))*(self.description.taxrate.taxrate/100)
        return qtetaxamount


################################3 Credit note ######################
# models.py (Credit Note related - NO SIGNIFICANT CHANGE, as it already applies to one company)

# Assuming existing: Company, Customer, Product, Invoice (Sales Invoice), Location
# And existing ChartOfAccount, JournalEntry, JournalEntryLine

class CommonCreditNotesModel(models.Model):
    company=models.ForeignKey(CommonCompanyDetailsModel, on_delete=models.CASCADE, related_name='cmpnycrdnt')
    customer=models.ForeignKey(CommonCustomersModel, on_delete=models.SET_NULL, related_name='cstmcrdtnot',null=True,blank=True)
    original_invoice=models.ForeignKey(CommonInvoicesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='credtnorgninv')
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    number=models.CharField(max_length=50, unique=True)
    total_amount=models.DecimalField(max_digits=30, decimal_places=2, default=0.00,null=True,blank=True)
    reasons=models.CharField(max_length=100,blank=False)
    status=models.CharField(max_length=50,choices=posting_status, default='waiting',null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvscrdtnte",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchcrdtnte",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptcrdtnte",on_delete=models.SET_NULL,null=True,blank=True)
    owner=models.ForeignKey(User, related_name="credntown",on_delete=models.SET_NULL,null=True,blank=True)
    return_location=models.ForeignKey(CommonSpacesModel, on_delete=models.SET_NULL, null=True, blank=True)
    
    approval_status=models.CharField(max_length=50,choices=approval_status, default='pending',null=True,blank=True)
    def __str__(self):
        return str(self.number)

class CommonCreditNoteItemsModel(models.Model):
    credit_note=models.ForeignKey(CommonCreditNotesModel, on_delete=models.CASCADE, related_name='crdntitems',null=True,blank=True)
    items=models.ForeignKey(CommonStocksModel, on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return str(self.credit_note)
    

class CommonTasksModel(models.Model):
    task=models.CharField(max_length=50,blank=False)
    status=models.CharField(max_length=10,choices=task_status,default='incomplete')
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    createDate=models.DateTimeField(auto_now_add=True)
    dueDate=models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)
    taskDay=models.CharField(max_length=10,choices=day,default='Monday')
    assignedto=models.ForeignKey(CommonEmployeesModel,on_delete=models.SET_NULL,blank=True,null=True,related_name="tskempl")
    owner=models.ForeignKey(User, related_name="cmnurtsk",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmntskscmpn",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvstasks",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchtasks",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="depttaskss",on_delete=models.SET_NULL,null=True,blank=True)
    description=models.CharField(blank=True,null=True,default='Task Description',max_length=50)
    
    def __str__(self):
    		return self.task

class CommonSalariesModel(models.Model):
    staff=models.ForeignKey(CommonEmployeesModel,related_name="stafsalrnm",on_delete=models.SET_NULL,null=True,blank=False)
    description=models.CharField(max_length=50,blank=False,null=True)
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    account=models.ForeignKey(CommonChartofAccountsModel,related_name="amsalrn",on_delete=models.SET_NULL,blank=False,null=True)
    status=models.CharField(choices=posting_status, default='waiting', max_length=100,blank=True,null=True)
    comments=models.CharField(max_length=30,blank=True,null=True)
    salary_payable=models.DecimalField(max_digits=30,blank=False,null=False,decimal_places=1,default=0)
    owner=models.ForeignKey(User, related_name="hrmslrnm",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmphrmrln",on_delete=models.SET_NULL,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvssalrs",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchslrs",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptslrss",on_delete=models.SET_NULL,null=True,blank=True)
    mode=models.ForeignKey(CommonPaymentTermsModel, related_name="salripymtn",on_delete=models.SET_NULL,null=True,blank=True)
    currency=models.ForeignKey(CommonCurrenciesModel, related_name="crrnslries",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
    	return str(self.staff)

class CommonJobsModel(models.Model):
    job_number=models.CharField(max_length=20,blank=True,null=True)
    owner=models.ForeignKey(User, related_name="jobsowner",on_delete=models.SET_NULL,null=True,blank=True)
    customer=models.ForeignKey(CommonCustomersModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='jobcustrelname')
    description=models.CharField(max_length=50,blank=True,null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpyjbs",on_delete=models.CASCADE,null=True,blank=True)
    opened_date=models.DateField(blank=True,null=True,auto_now_add=True)
    ending_date=models.DateField(blank=True,null=True,auto_now_add=False)
    status=models.CharField(max_length=20, blank=True, null=True,choices=job_status,default="open")
    comments=models.CharField(max_length=100,blank=True,null=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsjobss",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchjobss",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptjobs",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    payment_terms=models.ForeignKey(CommonPaymentTermsModel, related_name="jobpymtn",on_delete=models.SET_NULL,null=True,blank=True)
    currency=models.ForeignKey(CommonCurrenciesModel, related_name="crrncjob",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return str(self.job_number)


class CommonJobItemsModel(models.Model):
    item=models.ForeignKey(CommonStocksModel, blank=True, null=True, on_delete=models.CASCADE,related_name='itemjobcon')
    quantity=models.FloatField(max_length=20,blank=True,null=True,default=0)
    jobitemconnector= models.ForeignKey(CommonJobsModel, blank=True, null=True, on_delete=models.CASCADE,related_name='itemjobconrelnme')
    def __str__(self):
        return str(self.item)
    

#################################### shipments.... ###############

class CommonTransitModel(models.Model):
    owner=models.ForeignKey(User,related_name="shipment_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="shipment_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="shipment_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="shipment_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="shipment_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    description=models.CharField(max_length=50,blank=True,null=True)
    carrier=models.ForeignKey(CommonAssetsModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='carrier_related')
    
    date=models.DateField(auto_now_add=True,null=True,blank=True)
    expected=models.DateTimeField(null=True, blank=True)
    status=models.CharField(choices=Shipment_Status,null=True, blank=True, max_length=20,default="Booked")
    origin=models.CharField(null=True, blank=True, max_length=20)
    destination=models.CharField(null=True, blank=True, max_length=20)
    via=models.CharField(choices=Transport_Mode,null=True, blank=True, max_length=20,default="Road")
    shipment_number=models.CharField(null=True, blank=True, max_length=20)
    comments=models.CharField(blank=True,null=True,max_length=30)
    
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
         return '{}'.format(self.shipment_number)
 
class CommonTransitItemsModel(models.Model):
    """
    Individual items within a shipment, linked to CommonStocksModel.....
    """
    owner=models.ForeignKey(User,related_name="shipment_items_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="shipment_items_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="shipment_items_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="shipment_items_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="shipment_items_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    shipment=models.ForeignKey(CommonTransitModel,blank=True,null=True, on_delete=models.CASCADE, related_name='items')
    items=models.ForeignKey(CommonStocksModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipment_occurrences')
    quantity=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
   
    unit_of_measure=models.ForeignKey(CommonUnitsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='items_units_shipment')
    expected=models.DateTimeField(null=True, blank=True)
    expires=models.DateTimeField(null=True, blank=True)
    delivered_on=models.DateTimeField(null=True, blank=True)
    consigner= models.ForeignKey(CommonCustomersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='consignerrelated')
    consignee= models.ForeignKey(CommonCustomersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='consigneerelated')
    details=models.CharField(blank=True,null=True,max_length=200)
   
    weight=models.CharField(null=True, blank=True, max_length=50)
    
    length=models.CharField(null=True, blank=True, max_length=50)
    width=models.CharField(null=True, blank=True, max_length=50)
    height=models.CharField(null=True, blank=True, max_length=50)
    received= models.DateTimeField(null=True, blank=True)
    value=models.CharField(blank=True,null=True,max_length=50)
    rate=models.CharField(blank=True,null=True,max_length=50)
   
    status=models.CharField(choices=Shipment_Status,null=True, blank=True, max_length=20,default="Booked")
    origin= models.CharField(null=True, blank=True, max_length=50)
    destination= models.CharField(null=True, blank=True, max_length=50)
    comments= models.CharField(null=True, blank=True, max_length=50)
    
    
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

class CommonAssetCategoriesModel(models.Model):
    description=models.CharField(max_length=30,blank=False,null=True,unique=False)
    description=models.CharField(max_length=30,blank=False,null=True,unique=False)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="asstcatusr",blank=True,null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpasstcatasst",on_delete=models.CASCADE,null=True,blank=True)
    comments=models.CharField(null=True, blank=True, max_length=50)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsasstscats",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchasstscats",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptasstscats",on_delete=models.SET_NULL,null=True,blank=True)
 
    def __str__(self):
        return str(self.description)

class CommonProgramsModel(models.Model):# not used...may be deleted
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
    name=models.CharField(max_length=255,blank=True,null=True)
    code=models.CharField(max_length=50,blank=True,null=True, unique=False, help_text="Unique code for the program, e.g., BSCIT")
    description=models.CharField(blank=True, null=True,max_length=250)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    
    operation_year=models.ForeignKey(CommonOperationYearsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='program_operation_year')
    operation_term=models.ForeignKey(CommonOperationYearTermsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='terms_program')
    is_current=models.CharField(choices=operation_year_options,max_length=50,blank=True,null=True,default="Current")
   
    start_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    end_date=models.DateField(blank=True,null=True,default=timezone.localdate)
   
    owner=models.ForeignKey(User,related_name="ownr_programm",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmp_programs",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_programs",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_programs",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dept_programm",on_delete=models.SET_NULL,null=True,blank=True)
    

    def __str__(self):
        return str(self.name)

class CommonServicesModel(models.Model):# not used for now...may be deleted later
    
   
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
   
    code=models.CharField(max_length=50, help_text="Course code, e.g., CS101",blank=True,null=True)
    description=models.TextField(blank=True, null=True)
    credits=models.DecimalField(max_digits=4,blank=True,null=True, decimal_places=2, default=0.00, help_text="Credit hours for the course")
   
    operation_year=models.ForeignKey(CommonOperationYearsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='service_operation_year')
    operation_term=models.ForeignKey(CommonOperationYearTermsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='services_program')
    is_current=models.CharField(choices=operation_year_options,max_length=50,blank=True,null=True,default="Current")
   
    start_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    end_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    comments=models.CharField(blank=True,null=True, max_length=250)
    
    
    
    name=models.CharField(null=True, blank=True,max_length=250)
    unitprice=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    quantity=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    unitcost=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
   
    owner=models.ForeignKey(User,related_name="ownr_services",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmp_services",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_services",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_services",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dept_services",on_delete=models.SET_NULL,null=True,blank=True)
    
    
    normal_range_info=models.CharField(max_length=250, blank=True, null=True,help_text="General normal range information for this test (e.g., '70-110 mg/dL').")
    unit_of_measure=models.CharField(max_length=50, blank=True, null=True,help_text="Standard unit of measure for the test result (e.g., 'mg/dL', 'cells/mm3').")
    unit_of_measure=models.ForeignKey(CommonUnitsModel,related_name="unit_of_measure_services",on_delete=models.SET_NULL,null=True,blank=True)
    
  
    def __str__(self):
        return f"{self.name} ({self.code})"
    