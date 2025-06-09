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
    #branch=models.CharField(max_length=50,blank=True,null=True)
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
    

# --- Function to get the default Operation Year ---
def get_default_operation_year():
    """
    Returns the CommonOperationYearsModel instance marked as 'Current'.
    If multiple 'Current' years exist, it picks the latest one by 'start_date'.
    If no 'Current' year exists, it falls back to the overall latest year by 'start_date'.
    """
    try:
        # Try to find a year explicitly marked as 'Current'.
        # If there's a possibility of multiple 'Current' years (which should ideally be avoided
        # in practice), .latest('start_date') will pick the one with the most recent start_date.
        return CommonOperationYearsModel.objects.filter(is_current='Current').latest('start_date')
    except CommonOperationYearsModel.DoesNotExist:
        # If no year is explicitly marked 'Current', fall back to the overall latest year by its start_date.
        try:
            return CommonOperationYearsModel.objects.latest('start_date')
        except CommonOperationYearsModel.DoesNotExist:
            # If no operation years exist at all, print a warning and return None.
            # Returning None means the ForeignKey field must be defined with `null=True`.
            return None

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
   
    operation_year=models.ForeignKey(CommonOperationYearsModel,default=get_default_operation_year,blank=True,null=True, on_delete=models.CASCADE, related_name='termsyear')
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
    
# for educational institutions
class CommonFormsModel(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)
    owner=models.ForeignKey(User, related_name="cmnusfrm",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmnfrmcmp",on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=30,blank=True,null=True, default='comment')
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsforms",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchforms",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptforms",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.name

class CommonClassesModel(models.Model):
    form=models.ForeignKey(CommonFormsModel,on_delete=models.SET_NULL,blank=True,null=True)
    name=models.CharField(max_length=50,blank=True,null=True)
    contact=models.CharField(max_length=50,blank=True,null=True)
    size=models.IntegerField(blank=True,null=True)
    owner=models.ForeignKey(User, related_name="cmnusrclsrln",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmnclscmpy",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=30,blank=True,null=True, default='comment')
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsclsss",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchclss",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dptclss",on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.name


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
    form=models.ForeignKey(CommonFormsModel,on_delete=models.SET_NULL,blank=True,null=True)
    className=models.ForeignKey(CommonClassesModel,on_delete=models.SET_NULL,blank=True,null=True)
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
    status=models.CharField(choices=posting_status, default='waiting', max_length=20,blank=True,null=True)
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

















       
class CommonOrdersModel(models.Model):# very important model
    """
    healthcare....Represents a single visit or interaction a patient has with the healthcare facility.
    This acts as the central hub for all clinical activities during that specific encounter.
    sales... can represent sales orders, sales requisitions...
    education...can act as exam events, fees payment event etc
    services... service order to customers...
    realestate.... can act normal sales order when selling rents, properties, services etc..
    hospitality... can act as guest hosting event, customer orders from restaurents... etc
    """
    # general fields
    order_number=models.CharField(max_length=50, blank=False, null=True)
    employee_in_charge=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="encounters_as_primary_doctor",help_text="The main doctor attending this encounter.")
    customer=models.ForeignKey(CommonCustomersModel, on_delete=models.CASCADE,blank=True,null=True, related_name="medicalrecordcustmr",help_text="The patient associated with this encounter.")
    order_date_time=models.DateTimeField(auto_now_add=True,help_text="Date and time when this patient encounter record was created.",blank=True,null=True)
  
    # healthcare specific fields
    main_complaints=models.TextField(blank=True, null=True,help_text="The main reason for the patient's visit.")
    encounter_type=models.CharField(max_length=100,blank=True,null=True, choices=ENCOUNTER_TYPES, default='OUTP',help_text="Type of medical encounter (e.g., Outpatient, Inpatient, Emergency).")
    diagnosis=models.TextField(max_length=250,blank=True,null=True,default='diagnosis')
    end_date_time=models.DateTimeField(blank=True, null=True,help_text="Date and time when the encounter officially ended.")
    # Optional: Status of the encounter (e.g., 'Open', 'Closed', 'Pending')
    status=models.CharField(max_length=20,blank=True,null=True, default='Open',choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Pending', 'Pending')],help_text="Current status of the encounter.")

    # Common ERP fields (owner, company, division, branch, department)
    owner=models.ForeignKey(User, related_name="owned_encounters", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_encounters", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_encounters", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_encounters", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_encounters", on_delete=models.SET_NULL, null=True, blank=True)
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True) # Renamed for consistency
    diagnosis=models.TextField(max_length=250,blank=True,null=True,default='diagnosis')
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    
    start_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    end_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    is_current=models.CharField(choices=operation_year_options,max_length=50,blank=True,null=True,default="Current")
    
    description=models.CharField(max_length=255,blank=True,null=True)
    comments=models.CharField(max_length=255,blank=True,null=True)
    name=models.CharField(max_length=255,blank=True,null=True)
    code=models.CharField(max_length=50,blank=True,null=True, unique=False, help_text="Unique code for the program, e.g., BSCIT")
    
    operation_year=models.ForeignKey(CommonOperationYearsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='common_orders_operation_year')
    operation_term=models.ForeignKey(CommonOperationYearTermsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='terms_common_orders')
    
    
    def __str__(self):
        return f"Visit for {self.customer} ({self.encounter_type}) on {self.date.strftime('%Y-%m-%d %H:%M')}"
   
class CommonAssessmentTypesModel(models.Model):
    """
    Defines various assessment types as below.
    sales....physical conditions, dimensions of physical items...etc.
    Healthcare...checkup, doc observations, triage follow up etc.
    Education...QUIZ,EXAM,Assignment,Project,Participation,Other
    Hospitality...cleanliness, readyness etc etc
    Logistics...leakage, dents, physical conditions etc
    Realestate...physical, paint, general condition
    Services...physical, color, dents, location etc.
    
    """
    name=models.CharField(blank=True, null=True,max_length=250,default='assessment type')
    owner=models.ForeignKey(User, related_name="ownr_assessment_type",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpassessment_type",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsassessment_type",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchassessment_type",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptassessment_type",on_delete=models.SET_NULL,null=True,blank=True)
   
    def __str__(self):
        return str(self.name)
    
class CommonAssessmentsModel(models.Model):
    """
    Defines general assessments...
    staff... this can be used to assess the performance of staff members....
    sales...can be used to assess either staff or items... eg check the condition of bought items...
    Healthcare...doctor assessments on patients...
    Education...student assessments (e.g., Quizzes, Exams, Assignments).
    Logistics...item assessment... check the condition of the item when you receive and record...
    Realestate...building assessment, property assessment, construction assessment etc.
    Service...can be used for field assessments ...like audit assessment, financial assessments...
    .... this can be used to generate a general assessment report....
    """
    # general fields...
    person_assessing=models.ForeignKey(CommonEmployeesModel,related_name="person_assessing",on_delete=models.SET_NULL,null=True,blank=True)
    assessed_person=models.ForeignKey(CommonCustomersModel, on_delete=models.CASCADE, related_name='person_assessed',blank=True,null=True)
    operation_year=models.ForeignKey(CommonOperationYearsModel, on_delete=models.CASCADE, related_name='year_assessments',blank=True,null=True)
    order=models.ForeignKey(CommonOrdersModel, on_delete=models.CASCADE, related_name="mdclrcdobsv", blank=True, null=True,help_text="The encounter this triage record belongs to.")
  
    # healthcare specific fields.... like examination doctor field, patient field etc
    complaints=models.CharField(null=True, blank=True,max_length=250,help_text="Patient's main symptoms or reason for visit.")
    observations=models.CharField(null=True, blank=True,max_length=250)
   
    weight=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    # Added height for BMI calculation max_digits=5, decimal_places=2, blank=True, null=True,
    height=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,help_text="Patient's height in centimeters.")# normally in cm
    # Blood pressure separated for better data handling
    blood_pressure_systolic=models.IntegerField(blank=True, null=True,help_text="Systolic blood pressure (mmHg).")
    blood_pressure_diastolic=models.IntegerField(blank=True, null=True,help_text="Diastolic blood pressure (mmHg).")
    # temperatures are normally assumed to be in Celsius ... or specify the unit
    temperature=models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True,help_text="Patient's temperature in Celsius.")
    pulse_rate = models.IntegerField(blank=True, null=True,help_text="Patient's pulse rate (beats per minute).")
    respiration_rate = models.IntegerField(blank=True, null=True,help_text="Patient's respiration rate (breaths per minute).")
    oxygen_saturation = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True,help_text="Patient's oxygen saturation (SpO2 %).")

    chief_complaints = models.TextField(blank=True, null=True,help_text="Patient's main symptoms or reason for visit.")
    past_medical_history = models.TextField(blank=True, null=True,help_text="Relevant past medical history provided by the patient.")
    known_chronic_conditions_triage = models.TextField(blank=True, null=True,help_text="Patient's reported chronic conditions at triage.")
    # Consider linking to a structured MedicationHistoryModel instead of free text 'drugs'
    current_medications_at_triage = models.TextField(blank=True, null=True,help_text="Medications patient is currently taking, reported at triage.")

    triage_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date' to specific, auto_now_add
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True) # Changed to auto_now
    # Link to DiagnosesModel for structured diagnosis. Can be ManyToMany for multiple diagnoses.
    #diagnoses=models.ManyToManyField(CommonDiagnosesModel,help_text="Diagnoses made during this encounter.")
    
     # Added: Doctor's assessment/summary (A in SOAP)
    assessment=models.TextField(blank=True, null=True,help_text="Doctor's assessment of the patient's condition.")
    
     # Added: Treatment plan (P in SOAP)
    treatment_plan=models.TextField(blank=True, null=True,help_text="Treatment plan (medications, tests, referrals, follow-up).")

    observation_date_time=models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date', auto_now_add
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
    # test_From...like from blood, urine, stool, saliva etc
    test_from=models.ForeignKey(CommonCategoriesModel, max_length=200,blank=True,null=True,on_delete=models.CASCADE,related_name="lbtsfrm")
    test_for=models.ForeignKey(CommonCategoriesModel,blank=True,null=True, on_delete=models.CASCADE, related_name="patient_orders",help_text="The type of lab test ordered.")
    # Link to the MedicalServiceModel if this specific order is to be charged as a service
    charged_service=models.ForeignKey(CommonCategoriesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="labortry_order_charges",limit_choices_to={'service_type': 'LAB'},help_text="The specific medical service entry used for billing this lab test.")
    status=models.CharField(max_length=10,blank=True,null=True, choices=LAB_TEST_STATUSES, default='ORD',help_text="Current status of the lab test.")
    notes=models.TextField(blank=True, null=True) # For any specific notes related to the order

    
    # education specific fields...
    course=models.ForeignKey(CommonCategoriesModel, on_delete=models.CASCADE, related_name='course_assessments',blank=True,null=True)
    term=models.ForeignKey(CommonOperationYearTermsModel, on_delete=models.CASCADE, related_name='term_assessments',blank=True,null=True)
    name=models.CharField(max_length=255,blank=True,null=True)
    assessment_type = models.ForeignKey(CommonAssessmentTypesModel,  on_delete=models.CASCADE, related_name='type_assessments',blank=True,null=True)
    max_score=models.DecimalField(max_digits=5,blank=True,null=True, decimal_places=2)
    due_date=models.DateField(blank=True, null=True)
    
    owner=models.ForeignKey(User, related_name="ownr_assessmente",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpassessment",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsassessment",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchassessment",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptassessment",on_delete=models.SET_NULL,null=True,blank=True)
    
    # select the lab to do the test assuming there are many labs in the company
    #lab_name=models.ForeignKey(CommonLaboratoriesModel,blank=True,null=True, max_length=200,on_delete=models.CASCADE,related_name="labtlabtest")
    
    def __str__(self):
        return f"{self.name} for {self.course.code} ({self.term.name})"

class CommonResultsModel(models.Model):
    """
    Records various grades for assessments.
    sales...ok, needs attention etc
    healthcare...serve, normal, abnormal
    education...grades for students like A, B, C, 65%,87% etc...
    realestate...
    logistics...
    services...
    """
    # general fields....
    result_for_order=models.ForeignKey(CommonOrdersModel, on_delete=models.CASCADE, related_name="lab_orders", blank=True, null=True,help_text="The encounter this lab order belongs to.")
    result_owner=models.ForeignKey(CommonCustomersModel,blank=True,null=True, on_delete=models.CASCADE, related_name='grade_given_to')
    assessment=models.ForeignKey(CommonAssessmentsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='assessment_grades')
    result_given_by=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='grades_given_by')
    score=models.CharField(max_length=250,blank=True, null=True)
    comments=models.TextField(blank=True, null=True)
    test_from=models.ForeignKey(CommonCategoriesModel,blank=True,null=True, max_length=200,on_delete=models.CASCADE,related_name="lbtestreln")
    charged_service=models.ForeignKey(CommonCategoriesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="lab_order_charges",limit_choices_to={'service_type': 'LAB'},help_text="The specific medical service entry used for billing this lab test.")

    
    owner=models.ForeignKey(User, related_name="ownr_grades",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpgrades",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsgrades",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchgrades",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptgrades",on_delete=models.SET_NULL,null=True,blank=True)
   
    
    # healthcare fields...
    #lab_name=models.ForeignKey(CommonLaboratoriesModel,blank=True,null=True, max_length=200,on_delete=models.CASCADE,related_name="lab_result_con")
   
    expected_completion_date=models.DateField(blank=True, null=True)
    #Tracking status of the lab test
    status=models.CharField(max_length=10,blank=True,null=True, choices=LAB_TEST_STATUSES, default='ORD',help_text="Current status of the lab test.")
    notes=models.TextField(blank=True, null=True) # For any specific notes related to the order

    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    
     # Structured fields for results
    numerical_result=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,help_text="Numerical result of the test, if applicable.")
    
     # Unit of measure for the numerical result
    result_unit=models.CharField(max_length=50, blank=True, null=True,help_text="Unit of measure for the numerical result (e.g., 'mg/dL').")
     # Textual representation of normal range
    normal_range_text=models.CharField(max_length=100, blank=True, null=True,help_text="Normal range for this test result (e.g., '70-110').")
    is_abnormal=models.BooleanField(default=False,blank=True,null=True,help_text="True if the result is outside the normal range.")
    
     # For free-form interpretive text or qualitative results
    result_text=models.TextField(blank=True, null=True,help_text="Full textual result or interpretation.")
    
    result_date_time=models.DateTimeField(auto_now_add=True, blank=True, null=True) #  auto_now_add
    
     # Added: The lab technician/analyst who performed the test
    performed_by=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="performed_lab_results",help_text="The lab technician who entered the result.")
    
     # Added: The pathologist/doctor who validated the result
    validated_by=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="validated_lab_results",help_text="The doctor/pathologist who validated the result (optional).")
    
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)


    
    # education fields....
    
    
    def __str__(self):
        return f"Grade for {self.grade_given_to} "


class CommonTrackingModel(models.Model):
    """
    this is used to track various items, procedures, orders etc.
    sales... track items that are purchased or to be delivered...
    education... track student performance...
    Healthcare....Tracks the lifecycle of a lab sample from collection to archiving/disposal.
    """
    tracked_order=models.ForeignKey(CommonOrdersModel,blank=True,null=True, max_length=100,on_delete=models.CASCADE,related_name="labsmpletracking")
    owner=models.ForeignKey(User, related_name="ownrrsmpletracking",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpsmpletracking",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvssmpletracking",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchsmpletracking",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptsmpletracking",on_delete=models.SET_NULL,null=True,blank=True)
    
     # healthcare specific fields... each tracking collected samples..
    sample_number=models.CharField(max_length=100, unique=False, blank=True, null=True,help_text="Unique barcode or identifier for the physical sample.")
     # Added: Type/description of sample
    sample_description=models.CharField(max_length=50, choices=SAMPLE_TYPES, blank=True, null=True,help_text="Type of biological sample (e.g., Blood, Urine, Tissue).")
     #Current status of the sample
    status=models.CharField(max_length=50,blank=True,null=True, choices=LAB_TEST_STATUSES, default='SCOL', help_text="Current status of the sample (e.g., Collected, Received, Processing).")
    collection_date_time=models.DateTimeField(blank=True, null=True,help_text="Date and time when the sample was collected from the patient.")
    collected_by=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="collected_samples",help_text="The healthcare professional who collected the sample.")
    received_date_time=models.DateTimeField(blank=True, null=True,help_text="Date and time when the sample was received in the lab.")
    storage_location=models.CharField(max_length=250, blank=True, null=True,help_text="Physical location where the sample is stored (e.g., 'Fridge A, Shelf 2').")
    comments=models.TextField(blank=True, null=True,help_text="Any additional comments about the sample.")
    
    date_created=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
    
    ######### education specific fields... ########

    def __str__(self):
        return str(self.sample_number)

# --- Financial Models (Integration with CommonApp) ---



################################3assets######################################################

class CommonAssetCategoriesModel(models.Model):
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
class CommonAssetsModel(models.Model):
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
    category=models.ForeignKey(CommonAssetCategoriesModel, related_name="assetcat",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='asstdprmtn')
    employee_in_charge=models.ForeignKey(CommonEmployeesModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='asstemply')
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


###################3 credit/debit cards ###################33

class CommonCreditDebitCardsModel(models.Model):
    owner=models.ForeignKey(User,related_name="credit_debit_cards_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="credit_debit_cards_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="credit_debit_cards_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="credit_debit_cards_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="credit_debit_cards_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    card_name=models.CharField(max_length=15,blank=False,null=True)
    bank_issued=models.ForeignKey(CommonBanksModel,related_name="credit_debit_cards_bank",on_delete=models.SET_NULL,null=True,blank=True)
    number=models.IntegerField(null=True, blank=False,default=0)
    balance=models.IntegerField(null=True, blank=True,default=0)
    comment=models.CharField(max_length=15,blank=True,null=True,default='No comment')
    currency=models.ForeignKey(CommonCurrenciesModel,related_name="credit_debit_cards_currency",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return '{}'.format(self.card_name)
    
    def deposit(self, myamount):
        self.balance += myamount
        self.save()
    
    def withdraw(self, myamount):
        if myamount > self.balance:
            return HttpResponse("NO SUFFICIENT MONEY")
        self.balance -= myamount
        self.save()

class CommonTopUpCardsModel(models.Model):
    owner=models.ForeignKey(User,related_name="credit_debit_cards_top_up_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="credit_debit_cards_top_up_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="credit_debit_cards_top_up_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="credit_debit_cards_top_up_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="credit_debit_cards_top_up_department",on_delete=models.SET_NULL,null=True,blank=True)
    card= models.ForeignKey(CommonCreditDebitCardsModel,related_name="cardreltedname",on_delete=models.SET_NULL,blank=True,null=True)
    amount= models.IntegerField(null=True, blank=True,default=0)
    date=models.DateField(auto_now=True,blank=True,null=True)
    comments=models.CharField(max_length=15,blank=True,null=True, default='comment')
    
    def __str__(self):
        return '{}'.format(self.card)
   
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
   
#########################################3 STOCK ##############################################
class CommonWarehousesModel(models.Model):
    name=models.CharField(max_length=30, blank=False, null=True)
    owner=models.ForeignKey(User, related_name="wrhsown",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpnwhrns",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvswrhs",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchswrhss",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptswrhss",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    comments=models.CharField(null=True, blank=True, max_length=50)
    inventory_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='invaccwrhse')
    
    
    address=models.TextField(blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    capacity_sqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Storage capacity in square meters")
    emplyee_in_charge=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_warehouses')
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True,blank=True,null=True)


    def __str__(self):
    		return str(self.name) # this will show up in the admin area
 
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
    warehouse=models.ForeignKey(CommonWarehousesModel,related_name="stckwarehouse",on_delete=models.SET_NULL,null=True,blank=True)
    total_units_sold=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    ################### for medicals ##################
    
    #drugInvConnector= models.ForeignKey(GeneralInvoicesModel,related_name="druginvoiceconnector",on_delete=models.CASCADE,null=True,blank=True)
    drugDescription=models.CharField(null=True, blank=True, max_length=100)
    drugform=models.CharField(choices=DrugForm,default='Please selection', max_length=100,blank=True,null=True)
    drugUnit=models.CharField(choices=DrugUnits,default='Please selection', max_length=100,blank=True,null=True)
   
    drug_notes=models.CharField(blank=True,null=True,default="notes",max_length=250)
    
    code=models.CharField(max_length=50, help_text="Course code, e.g., CS101",blank=True,null=True)
    
    credits=models.DecimalField(max_digits=4,blank=True,null=True, decimal_places=2, default=0.00, help_text="Credit hours for the course")
   
    operation_year=models.ForeignKey(CommonOperationYearsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='stocks_operation_year')
    operation_term=models.ForeignKey(CommonOperationYearTermsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='stocks_program')
    is_current=models.CharField(choices=operation_year_options,max_length=50,blank=True,null=True,default="Current")
   
    start_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    end_date=models.DateField(blank=True,null=True,default=timezone.localdate)
    comments=models.CharField(blank=True,null=True, max_length=250)
    
    # this field helps a lot.. for instance when invoicing, it will only affect current stock if it  is a physical item
    # if it is service, it will invoice but it will not affect the current stock as it is intangible
    item_is_physical_or_service=models.CharField(choices=item_in_physical_state_or_service,max_length=50,blank=True,null=True,default="Current")
   
    
    
    name=models.CharField(null=True, blank=True,max_length=250)
   
    
    normal_range_info=models.CharField(max_length=250, blank=True, null=True,help_text="General normal range information for this test (e.g., '70-110 mg/dL').")
   
    unit_of_measure=models.ForeignKey(CommonUnitsModel,related_name="unit_of_measure_stocks",on_delete=models.SET_NULL,null=True,blank=True)
    
    
    

    class Meta:
        # THIS IS THE CRUCIAL ADDITION/CONFIRMATION
        unique_together = ('company', 'partNumber', 'warehouse')
        
    def __str__(self):
    		return str(self.description) # this will show up in the admin area

class CommonWarehouseItemsModel(models.Model):
    warehouse=models.ForeignKey(CommonWarehousesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='wrhseitms')
    items=models.ForeignKey(CommonStocksModel,blank=False,null=False, on_delete=models.CASCADE,related_name='wrhseitemsstck')
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=2,default=0)
    class Meta:
        # THIS IS THE CRUCIAL ADDITION/CONFIRMATION
        unique_together = ('items', 'warehouse')
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
 
    from_store=models.ForeignKey(CommonWarehousesModel,related_name="frmintcmpstcktrnsfrs",on_delete=models.SET_NULL,null=True,blank=True)
    to_store=models.ForeignKey(CommonWarehousesModel,related_name="tointcmpstcktrnsfrs",on_delete=models.SET_NULL,null=True,blank=True)
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

################# PROPERTIES SECTION ############3

##############3 properties ##############3
class CommonPropertiesModel(models.Model):
    """
    Represents a physical property (e.g., a building, a plot of land, a mall).
    """
    owner=models.ForeignKey(User,related_name="ownr_properties",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmp_properties",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_properties",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_properties",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dept_properties",on_delete=models.SET_NULL,null=True,blank=True)
    
    name=models.CharField(max_length=255,blank=True,null=True, help_text="Common name or identifier for the property (e.g., 'Maple Apartments', 'Downtown Mall')")
    property_type=models.ForeignKey(CommonCategoriesModel,related_name="dept_properties",on_delete=models.SET_NULL,null=True,blank=True)
    address=models.TextField(help_text="Full street address of the property",blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    state=models.CharField(max_length=100, blank=True, null=True)
    zip_code=models.CharField(max_length=20, blank=True, null=True)
    country=models.CharField(max_length=100, default="Somalia",blank=True,null=True) # Default for your context
    total_area_sqft=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Total area of the property in square feet")
    purchase_date=models.DateField(blank=True, null=True)
    purchase_price=models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    description=models.TextField(blank=True, null=True)
    is_active=models.BooleanField(default=True,blank=True,null=True, help_text="Is this property currently managed?")

    def __str__(self):
        return f"{self.name} ({self.property_type}) - {self.city}"

class CommonPropertyUnitsModel(models.Model):
    """
    Represents an individual unit within a property (e.g., apartment #101, shop #A5, office floor).
    Only applicable for multi-unit properties.
    """
    property=models.ForeignKey(CommonPropertiesModel,blank=True,null=True, on_delete=models.CASCADE, related_name='units')
    unit_number=models.CharField(max_length=50,blank=True,null=True, help_text="Unique identifier for the unit within the property (e.g., '101', 'Shop A5')")
    unit_type=models.CharField(max_length=10,blank=True,null=True, choices=PROPERTY_UNIT_TYPES)
    number_of_bedrooms=models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_bathrooms=models.PositiveSmallIntegerField(blank=True, null=True)
    area_sqft=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_price=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Monthly rental price for the unit")
    is_available=models.BooleanField(default=True,blank=True,null=True, help_text="Is this unit currently available for rent/sale?")
    description=models.TextField(blank=True, null=True)
    
    owner=models.ForeignKey(User,related_name="ownr_property_unit_types",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmp_property_unit_types",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_property_unit_types",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_property_unit_types",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dept_property_unit_types",on_delete=models.SET_NULL,null=True,blank=True)
    
    
    def __str__(self):
        return f"{self.unit_number} at {self.property.name}"


class CommonLeaseAgreementsModel(models.Model):
    """
    Details of a lease agreement between a tenant and a property/unit.
    """
    property=models.ForeignKey(CommonPropertiesModel,blank=True,null=True, on_delete=models.CASCADE, related_name='leases', help_text="The property being leased (if a whole property or land)")
    tenant=models.ForeignKey(CommonCustomersModel,blank=True,null=True, on_delete=models.CASCADE, related_name='leases')
    unit=models.ForeignKey(CommonPropertyUnitsModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='leases', help_text="The specific unit being leased (if applicable)")
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(blank=True, null=True)
    monthly_rent=models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2)
    security_deposit=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0.00')
    payment_due_day=models.PositiveSmallIntegerField(default=1,blank=True,null=True, help_text="Day of the month rent is due (e.g., 1 for 1st of month)")
    terms_and_conditions=models.TextField(blank=True, null=True)
    is_active=models.BooleanField(default=True,blank=True,null=True)
    # Link to CommonPaymentTermsModel if you have defined terms like NET30, NET60 etc.
    # payment_terms = models.ForeignKey(CommonPaymentTermsModel, on_delete=models.SET_NULL, null=True, blank=True)
    owner=models.ForeignKey(User,related_name="ownr_lease_agrement",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmp_lease_agrement",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_lease_agrement",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_lease_agrement",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dept_lease_agrement",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
       return str(self.tenant)

class CommonConstructionProjectsModel(models.Model):
    """
    Manages details of a construction or major renovation project.
    """
    project_name=models.CharField(max_length=255,blank=True,null=True)
    property=models.ForeignKey(CommonPropertiesModel,blank=True,null=True, on_delete=models.CASCADE, related_name='construction_projects', help_text="The property where construction is taking place")
    start_date=models.DateField(blank=True,null=True)
    expected_end_date=models.DateField(blank=True,null=True)
    actual_end_date=models.DateField(blank=True, null=True)
    budget_amount=models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    current_cost=models.DecimalField(max_digits=15,blank=True,null=True, decimal_places=2, default='0.00')
    project_manager=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_projects')
    status = models.CharField(max_length=10,blank=True,null=True, choices=PROJECT_STATUS_CHOICES, default='PLAN')
    description = models.TextField(blank=True, null=True)
    
    owner=models.ForeignKey(User,related_name="ownr_prject",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmp_prject",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvs_prject",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnch_prject",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dept_prject",on_delete=models.SET_NULL,null=True,blank=True)
    

    def __str__(self):
        return f"{self.project_name} on {self.property.name} ({self.status})"

class CommonProjectTasksModel(models.Model):
    """
    Individual tasks within a construction project.
    """
    owner=models.ForeignKey(User,related_name="project_tasks_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="project_tasks_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="project_tasks_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="project_tasks_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="project_tasks_dept",on_delete=models.SET_NULL,null=True,blank=True)
    

    construction_project=models.ForeignKey(CommonConstructionProjectsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='tasks')
    task_name=models.CharField(max_length=255,blank=True,null=True)
    description=models.TextField(blank=True, null=True)
    assigned_to=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    start_date=models.DateField(blank=True, null=True)
    due_date=models.DateField(blank=True, null=True)
    completion_date=models.DateField(blank=True, null=True)

    
    # options for this field are like planned, onhold, compelted...
    status=models.CharField(max_length=10,blank=True,null=True, choices=STATUS_CHOICES)
    
    priority_level=models.CharField(max_length=10,blank=True,null=True, choices=PRIORITY_TYPES)
    spares_cost=models.IntegerField(blank=True,null=True,default=0)
    labor_cost=models.IntegerField(blank=True,null=True,default=0)
   
    def __str__(self):
        return f"{self.task_name} for {self.construction_project.project_name} ({self.status})"


class CommonPropertyStatusModel(models.Model):
    """
    Represents a property listing for sale or rent.
    """
    owner=models.ForeignKey(User,related_name="property_listings_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="property_listings_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="property_listings_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="property_listings_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="property_listings_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    property=models.ForeignKey(CommonPropertiesModel,blank=True,null=True, on_delete=models.CASCADE, related_name='listings')
    listing_type=models.CharField(max_length=10,blank=True,null=True, choices=PROPERTY_STATUS_TYPES)
    listing_price=models.DecimalField(max_digits=15,blank=True,null=True, decimal_places=2, help_text="Asking price for sale or monthly rent")
    listing_agent=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='property_listings', help_text="The realtor/agent handling this listing")
    listing_date=models.DateField(auto_now_add=True,blank=True,null=True)
    expiration_date=models.DateField(blank=True, null=True)
   
    description=models.TextField(blank=True, null=True, help_text="Detailed description for the listing")
    # You might want to add fields for images, virtual tours etc.

    def __str__(self):
        return str(self.property)


class CommonRoomTypesModel(models.Model):
    """
    this is for normal hotels, shopping malls etc
    """
    #Defines categories of rooms (e.g., Standard, Deluxe, Suite).
    owner=models.ForeignKey(User, related_name="owned_room_type", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_room_type", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_room_types", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_room_type", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_room_type", on_delete=models.SET_NULL, null=True, blank=True)
    
    name=models.CharField(max_length=100,blank=True,null=True)
    description=models.TextField(blank=True, null=True)
    base_price_per_night=models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2)
    max_occupancy=models.PositiveSmallIntegerField(default=2,blank=True,null=True)
    amenities=models.TextField(blank=True, null=True, help_text="e.g., WiFi, AC, Balcony, Minibar")
    is_active=models.BooleanField(default=True,blank=True,null=True)
    date=models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of note-taking
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return str(self.name)

class CommonRoomsModel(models.Model):
    #Represents an individual hotel room.
    owner=models.ForeignKey(User, related_name="owned_rooms", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_rooms", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_rooms", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_rooms", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_rooms", on_delete=models.SET_NULL, null=True, blank=True)
    
    room_number=models.CharField(max_length=50,blank=True,null=True)
    room_type=models.ForeignKey(CommonRoomTypesModel,blank=True,null=True, on_delete=models.PROTECT, related_name='rooms') # PROTECT to prevent deleting room type if rooms exist
    floor=models.PositiveSmallIntegerField(choices=FLOOR_CHOICES, blank=True, null=True)
    
    current_status = models.CharField(max_length=10,blank=True,null=True, choices=CURRENT_STATUS_CHOICES, default='AVAIL')
    notes=models.TextField(blank=True, null=True)
    is_active=models.BooleanField(default=True,blank=True,null=True)
    date=models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of note-taking
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return f"Room {self.room_number} ({self.room_type.name})"

class CommonEventHallsModel(models.Model):
    #Represents an individual hotel room.
    owner=models.ForeignKey(User, related_name="owned_event_halls", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_event_halls", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_event_halls", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_event_halls", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_event_halls", on_delete=models.SET_NULL, null=True, blank=True)
    
    hall_number=models.CharField(max_length=50,blank=True,null=True)
    room_type=models.ForeignKey(CommonRoomTypesModel,blank=True,null=True, on_delete=models.PROTECT, related_name='event_halls') # PROTECT to prevent deleting room type if rooms exist
    floor=models.PositiveSmallIntegerField(choices=FLOOR_CHOICES, blank=True, null=True)
    
    current_status = models.CharField(max_length=10,blank=True,null=True, choices=CURRENT_STATUS_CHOICES, default='AVAIL')
    notes=models.TextField(blank=True, null=True)
    is_active=models.BooleanField(default=True,blank=True,null=True)
    date=models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of note-taking
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return f"Room {self.hall_number} ({self.room_type.name})"

class CommonRoomBookingsModel(models.Model):
    #Represents a room booking.
    owner=models.ForeignKey(User, related_name="owned_room_booking", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_room_booking", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_room_booking", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_room_booking", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_room_booking", on_delete=models.SET_NULL, null=True, blank=True)
    
    name=models.ForeignKey(CommonCustomersModel,blank=True,null=True, on_delete=models.CASCADE, related_name='bookings_custmr')
    room=models.ForeignKey(CommonRoomsModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings') # Nullable if room not assigned yet
    check_in_date_time=models.DateTimeField(blank=True,null=True)
    check_out_date=models.DateTimeField(blank=True,null=True)
    number_of_adults=models.PositiveSmallIntegerField(default=1,blank=True,null=True)
    number_of_children=models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    total_price=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Calculated total price for the stay")
   
    status=models.CharField(max_length=10,blank=True,null=True, choices=BOOKING_STATUS_CHOICES, default='PEND')
    booking_notes=models.TextField(blank=True, null=True)
    
    date=models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of note-taking
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.name} at ({{ self.check_in_date }} - {{ self.check_out_date }})"

    def clean(self):
        # Basic validation for check-in/out dates
        if self.check_in_date_time and self.check_out_date and self.check_in_date_time >= self.check_out_date:
            raise models.ValidationError("Check-out date must be after check-in date.")


# --- Restaurant/F&B Models ---
class CommonRestaurantsModel(models.Model):
    """
    Represents a restaurant or food & beverage outlet within a hotel or standalone.
    """
    owner=models.ForeignKey(User, related_name="owned_restaurant", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_restaurant", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_restaurant", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_restaurant", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_restaurant", on_delete=models.SET_NULL, null=True, blank=True)
    name=models.CharField(max_length=250,blank=True,null=True)
    contact_phone=models.CharField(max_length=20, blank=True, null=True)
    description=models.TextField(blank=True, null=True)
    date=models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of note-taking
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)

   
    def __str__(self):
        restaurant_info = f"({self.name})" if self.description else ""
        return f"{self.name} {restaurant_info} - {self.company.company}"

class CommonRecipesModel(models.Model):
    owner=models.ForeignKey(User, related_name="owned_recipes", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_recipes", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_recipes", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_recipes", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_recipes", on_delete=models.SET_NULL, null=True, blank=True)
    name=models.CharField(max_length=220,blank=True,null=True)
    description=models.TextField(blank=True, null=True)
    directions=models.TextField(blank=True, null=True)
    timestamp=models.DateTimeField(auto_now_add=True,blank=True,null=True) 
    updated=models.DateTimeField(auto_now=True,blank=True,null=True) 
    active=models.BooleanField(default=True,blank=True,null=True)
    def __str__(self):
        return self.name

  
class CommonRecipeIngredientsModel(models.Model):
    owner=models.ForeignKey(User, related_name="owned_ingredients", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_ingredients", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_ingredients", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_ingredients", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_ingredients", on_delete=models.SET_NULL, null=True, blank=True)
    recipe=models.ForeignKey(CommonRecipesModel,blank=True,null=True, on_delete=models.CASCADE)
   
    name=models.CharField(max_length=220,blank=True,null=True)
    description=models.TextField(blank=True, null=True)
    quantity=models.CharField(max_length=50, blank=True, null=True)  # 1 1/4
    quantity_as_decimal=models.DecimalField(max_digits=30,decimal_places=2,blank=True, null=True)
    # pounds, lbs, oz, gram, etc
    units=models.ForeignKey(CommonUnitsModel, related_name="ingredients_units", on_delete=models.CASCADE, null=True, blank=True)
   
    timestamp=models.DateTimeField(auto_now_add=True,blank=True,null=True) 
    updated=models.DateTimeField(auto_now=True,blank=True,null=True) 
    
    def get_absolute_url(self):
        return self.recipe.get_absolute_url()
    
class CommonMenuCategoriesModel(models.Model):
    """
    Categorizes menu items (e.g., Appetizers, Main Course, Drinks).
    """
    owner=models.ForeignKey(User, related_name="owned_menu_category", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_menu_category", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_menu_category", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_menu_category", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_menu_category", on_delete=models.SET_NULL, null=True, blank=True)
    restaurant=models.ForeignKey(CommonRestaurantsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='menu_item_categories')
    name=models.CharField(max_length=100,blank=True,null=True)
    date=models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of note-taking
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name}) - {self.company.company}"

class CommonMenuItemsModel(models.Model):
    """
    Individual items on a restaurant's menu.
    """
    restaurant=models.ForeignKey(CommonRestaurantsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='menu_items')
    category=models.ForeignKey(CommonMenuCategoriesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='menu_items')
    name=models.CharField(max_length=255,blank=True,null=True)
    description=models.TextField(blank=True, null=True)
    price=models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2)
    is_available=models.BooleanField(default=True,blank=True,null=True)
    # Link to CommonStocksModel for ingredients if managing recipe costs
    # ingredients = models.ManyToManyField(CommonStocksModel, through='MenuItemIngredient', blank=True)

   
    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

class CommonRestaurantTablesModel(models.Model):
    """
    Represents a table in a restaurant.
    """
    restaurant=models.ForeignKey(CommonRestaurantsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='tables')
    table_number=models.CharField(max_length=50,blank=True,null=True)
    capacity=models.PositiveSmallIntegerField(default=1,blank=True,null=True)
    table_location=models.CharField(max_length=255, blank=True, null=True, help_text="e.g., 'Window Side', 'Patio'")
    status=models.CharField(max_length=10,blank=True,null=True, choices=STATUS_CHOICES, default='AVAIL')
    is_active=models.BooleanField(default=True,blank=True,null=True)

    def __str__(self):
        return f"Table {self.table_number} ({self.restaurant.name})"

class CommonRestaurantOrdersModel(models.Model):
    """
    Represents a customer's order in a restaurant.
    """
    restaurant=models.ForeignKey(CommonRestaurantsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='orders')
    customer=models.ForeignKey(CommonCustomersModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='restaurant_orders', help_text="Can be a guest or walk-in customer")
    table=models.ForeignKey(CommonRestaurantTablesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    order_number=models.CharField(max_length=50, unique=True, blank=True, null=True)
    order_date_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    total_amount=models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2, default=Decimal('0.00'))
    
    status=models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES,blank=True,null=True, default='PEND')
    served_by=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_served')
    notes=models.TextField(blank=True, null=True)

    def __str__(self):
        table_info = f"Table {self.table.table_number}" if self.table else "Delivery"
        return f"Order #{self.order_number or self.pk} for {self.customer.name if self.customer else 'Walk-in'} ({table_info}) ({self.total_amount()}) - {self.table}"

class CommonRestaurantOrderItemsModel(models.Model):
    """
    Individual items within a restaurant order.
    """
    order=models.ForeignKey(CommonRestaurantOrdersModel,blank=True,null=True, on_delete=models.CASCADE, related_name='items')
    menu_item=models.ForeignKey(CommonMenuItemsModel,blank=True,null=True, on_delete=models.SET_NULL, related_name='ordered_items') # PROTECT to prevent deleting menu item if ordered
    quantity=models.PositiveSmallIntegerField(default=1,blank=True,null=True)
    unit_price=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    preparation_notes=models.TextField(blank=True, null=True, help_text="e.g., 'No onions', 'Well done'")
    status = models.CharField(max_length=10,blank=True,null=True, choices=STATUS_CHOICES_STATE, default='PEND')

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order #{self.order.order_number or self.order.pk}"

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.menu_item.price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Recalculate parent order's total_amount
        self.order.total_amount = sum(self.total_price for item in self.order.items.all())
        self.order.save()


class CommonRestaurantInvoice(models.Model):
    """
    Invoice generated for a restaurant order, linked to CommonInvoicesModel.
    """
    order = models.OneToOneField(CommonRestaurantOrdersModel,blank=True,null=True, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    invoice_date = models.DateField(auto_now_add=True,blank=True,null=True)
    due_date = models.DateField(blank=True,null=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True, default=Decimal('0.00'))
    balance_due = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    
    status = models.CharField(max_length=10,blank=True,null=True, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True)

    # Link to CommonInvoicesModel
    common_invoice = models.OneToOneField('CommonInvoicesModel',blank=True,null=True, on_delete=models.CASCADE, related_name='restaurant_invoice')

    def __str__(self):
        return f"Restaurant Invoice #{self.invoice_number or self.pk} for Order {self.order.order_number or self.order.pk} ({self.status})"

class CommonKitchenProductionsModel(models.Model):
    """
    Tracks production of dishes/menu items in the kitchen (for inventory deduction).
    """
    restaurant=models.ForeignKey(CommonRestaurantsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='production_logs')
    menu_item=models.ForeignKey(CommonMenuItemsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='production_logs')
    quantity_produced=models.PositiveSmallIntegerField(blank=True,null=True)
    production_date_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    produced_by=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, help_text="Chef/Cook who produced it")
    notes=models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Produced {self.quantity_produced} x {self.menu_item.name} at {self.restaurant.name} on {self.production_date_time.date()}"


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


##################### MATERIAL REQUISITIONS #######################
class CommonMaterialRequisitionsModel(models.Model):
    """
    Represents a request for materials or stock items from inventory.
    This is the header record for a material requisition.
    """
    owner=models.ForeignKey(User,related_name="requisition_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="requisition_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="requisition_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="requisition_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="requisition_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    # Requisition Identifier
    requisition_number=models.CharField(max_length=100, unique=True, null=False, blank=False,help_text="Unique identifier for this material requisition (e.g., 'MR-2023-001').")

    # Request Originator
    requested_by_employee=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,help_text="The employee who initiated this material requisition.")
    # The requesting department might differ from the owner's department in CommonBaseModel
    requesting_department=models.ForeignKey(CommonDepartmentsModel, on_delete=models.SET_NULL, null=True, blank=True,help_text="The department for which these materials are requested.")

    # Purpose and Context
    purpose=models.TextField(null=False, blank=False,help_text="Brief description of the purpose for this material requisition.")
    project_or_cost_center=models.CharField(max_length=255, blank=True, null=True,help_text="Optional: The project or cost center this requisition is for.")

    # Dates
    required_by_date = models.DateField(null=False, blank=False,help_text="The date by which the requested materials are needed.")

    # Status and Approval
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', null=False, blank=False,help_text="Current status of the material requisition.")
    
    approved_by=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name='approved_material_requisitions',help_text="The employee who approved this requisition.")
    approval_date=models.DateTimeField(blank=True, null=True,help_text="Date and time when the requisition was approved.")

    # Fulfillment Summary
    is_fully_fulfilled=models.BooleanField(default=False, null=False, blank=False,help_text="Indicates if all items on this requisition have been fulfilled.")
    fulfillment_notes=models.TextField(blank=True, null=True,help_text="Any general notes regarding the fulfillment of this requisition.")

    # General Notes for the entire requisition
    comments=models.TextField(blank=True, null=True,help_text="Any additional general notes about this material requisition.")

  
  
    def __str__(self):
        return f"MR #{self.requisition_number} "

    def save(self, *args, **kwargs):
        # Generate a unique requisition number if not provided (example logic)
        if not self.requisition_number:
            today = timezone.now().strftime('%Y%m%d')
            # Assuming a way to get a sequential number for the day
            # This is a simplified example; in production, use FSM or database sequence
            last_req=CommonMaterialRequisitionsModel.all_objects.filter(company=self.company,date_created__date=timezone.now().date()).order_by('-requisition_number').first()
            
            if last_req and last_req.requisition_number.startswith(f'MR-{today}-'):
                last_seq=int(last_req.requisition_number.split('-')[-1])
                new_seq=last_seq + 1
            else:
                new_seq = 1
            self.requisition_number = f'MR-{today}-{new_seq:04d}'
        super().save(*args, **kwargs)


class CommonMaterialRequisitionItemsModel(models.Model):
    """
    Represents an individual line item within a CommonMaterialRequisitionModel.
    It details the specific material requested and its quantities.
    """
    requisition=models.ForeignKey(CommonMaterialRequisitionsModel, on_delete=models.CASCADE, null=False, blank=False,help_text="The material requisition to which this item belongs.")
    
    material=models.ForeignKey(CommonStocksModel, on_delete=models.PROTECT, null=False, blank=False,help_text="The specific material/stock item being requested.")
    
    # Material description (can be auto-filled from material.item_name but allow override)
    description=models.TextField(blank=True, null=True,help_text="Detailed description of the requested material (can override stock item description).")

    # Quantities and Units
    quantity_requested=models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,help_text="The quantity of the material requested.")
    unit_of_measure=models.CharField(max_length=50, null=False, blank=False,help_text="The unit of measure for the requested quantity (e.g., 'Pcs', 'Kg', 'Rolls').")
    
    quantity_approved=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="The quantity of the material approved for issue (can be less than requested).")
    quantity_fulfilled=models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), null=False, blank=False,help_text="The actual quantity of the material issued/fulfilled so far.")

    # Item Status and Notes
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', null=False, blank=False,help_text="Current status of this specific line item.")
    item_notes=models.TextField(blank=True, null=True,help_text="Any specific notes for this individual requested item.")
    
    # Audit fields for the line item (distinct from header, though often inherited or auto-set)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

   
   
   
    def __str__(self):
        return f"{self.quantity_requested} {self.unit_of_measure} of {self.material.item_name} for MR #{self.requisition.requisition_number}"

    def save(self, *args, **kwargs):
        # Auto-fill quantity_approved if not set, and set to requested
        if self.quantity_approved is None:
            self.quantity_approved = self.quantity_requested
        
        # Ensure unit_of_measure is not blank if material exists and has one
        if not self.unit_of_measure and self.material and self.material.unit_of_measure:
            self.unit_of_measure = self.material.unit_of_measure

        super().save(*args, **kwargs)
        # You might add logic here or use signals to update the parent requisition's status
        # e.g., if all items are fulfilled, update requisition.is_fully_fulfilled

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


####################### commisions #######################

class CommonCommissionsModel(models.Model):
    """
    Records commission earned on a successful various business operations by various staff members.
    """
    owner=models.ForeignKey(User,related_name="commissions_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="commissions_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="commissions_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="commissions_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="commissions_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    commision_description=models.CharField(max_length=250,blank=True,null=True)
    agent=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='commissions_earned')
    commission_percentage=models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="e.g., 2.50 for 2.5%")
    commission_amount=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    transaction_date=models.DateField(blank=True, null=True, help_text="Date of sale/rental closing")
    
    status=models.CharField(max_length=10, choices=payment_status,blank=True,null=True, default='PENDING')

    def __str__(self):
        return f"Commission for {self.agent}"

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
    return_location=models.ForeignKey(CommonWarehousesModel, on_delete=models.SET_NULL, null=True, blank=True)
    
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
    

class CommonMaintenanceRequestsModel(models.Model):
    """
    Requests from tenants or staff for property maintenance.
    """
    owner=models.ForeignKey(User,related_name="maintenance_request_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="maintenance_request_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="maintenance_request_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="maintenance_request_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="maintenance_request_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    maintenance_number=models.CharField(max_length=30,blank=True,null=True)
    customer=models.ForeignKey(CommonCustomersModel,blank=True,null=True, on_delete=models.CASCADE, related_name='maintenance_requests_customer')
    reported_by_employee=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='issued_maintenance_requests')
    description=models.TextField(help_text="Detailed description of the issue",blank=True,null=True)
    request_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    priority=models.CharField(max_length=10,blank=True,null=True, choices=PRIORITY_TYPES, default='MED')
    
    status=models.CharField(max_length=10,blank=True,null=True, choices=STATUS_CHOICES, default='OPEN')
    notes=models.TextField(blank=True, null=True, help_text="Internal notes on the request")
    
    
    
    equipment=models.ForeignKey(CommonAssetsModel,on_delete=models.SET_NULL,blank=True,null=True)
    date=models.DateField(blank=True,null=True,auto_now=True)
    odometer=models.IntegerField(blank=True,null=True)
   
    service_center= models.CharField(max_length=30, blank=True, null=True)

    service_cost=models.DecimalField(max_digits=10,blank=True,null=True,decimal_places=2,default=0)
    
    serviced_by=models.CharField(blank=True,null=True,max_length=20)
   
    notes=models.CharField(blank=True,null=True,max_length=20)

    def __str__(self):
        return str(self.customer)

class CommonMaintenanceAssignmentsModel(models.Model):
    """
    A planned or executed job to address one or more maintenance requests.
    """
    owner=models.ForeignKey(User,related_name="job_assignment_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="job_assignment_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="job_assignment_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="job_assignment_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="job_assignment_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    maintenance_requests=models.ManyToManyField(CommonMaintenanceRequestsModel, related_name='maintenance_jobs', help_text="Requests addressed by this job")
    job_title=models.CharField(max_length=255,blank=True,null=True)
    description=models.TextField(blank=True, null=True)
    assigned_to_employee=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_maintenance_jobs', help_text="Internal employee assigned to the job")
    assigned_to_vendor=models.ForeignKey(CommonSuppliersModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_maintenance_jobs_vendor', help_text="External vendor/supplier assigned to the job") # Assuming vendors are also customers
    scheduled_date=models.DateField(blank=True, null=True)
    completion_date=models.DateField(blank=True, null=True)
    estimated_cost=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    actual_cost=models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
   
    status = models.CharField(max_length=10,blank=True,null=True, choices=PROJECT_STATUS_CHOICES, default='PLAN')
    
   
    def __str__(self):
        return str(self.job_title)
 

class CommonShipmentsModel(models.Model):
    owner=models.ForeignKey(User,related_name="shipment_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="shipment_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="shipment_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="shipment_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="shipment_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    carrier=models.ForeignKey(CommonAssetsModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='carrier_related')
    date=models.DateTimeField(null=True, blank=True)
    expected= models.DateTimeField(null=True, blank=True)
    status= models.CharField(choices=Shipment_Status,null=True, blank=True, max_length=20,default="Booked")
    origin= models.CharField(null=True, blank=True, max_length=20)
    destination= models.CharField(null=True, blank=True, max_length=20)
    via= models.CharField(choices=Transport_Mode,null=True, blank=True, max_length=20,default="Road")
    shipment_number= models.CharField(null=True, blank=True, max_length=20)
    comments=models.CharField(blank=True,null=True,max_length=30)
    
    exit_warehouse=models.ForeignKey(CommonWarehousesModel,blank=True,null=True, on_delete=models.CASCADE, related_name='exits')
    entry_warehouse=models.ForeignKey(CommonWarehousesModel,blank=True,null=True, on_delete=models.CASCADE, related_name='entries')
    
    dispatched_by=models.ForeignKey(CommonEmployeesModel,related_name='shipment_dispatched_by', on_delete=models.SET_NULL, null=True, blank=True)
    customer=models.ForeignKey(CommonCustomersModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='goods_received')
    
    notes=models.TextField(blank=True, null=True)
    
    unit_of_measure=models.CharField(max_length=50, blank=True, null=True)
    entry_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    received_by=models.ForeignKey(CommonEmployeesModel,related_name='shipment_received_by', on_delete=models.SET_NULL, null=True, blank=True)
    supplier=models.ForeignKey(CommonCustomersModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='goods_supplied') # Assuming suppliers are customers
    notes=models.TextField(blank=True, null=True)
    
    delivery_confirmed_by_customer=models.ForeignKey(CommonCustomersModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_deliveries_customer')
    delivery_confirmed_by_employee=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_deliveries_employee')
    delivery_confirmation_date_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    delivery_notes=models.TextField(blank=True, null=True)
  
    def __str__(self):
         return '{}'.format(self.shipment_number)
 
 
class CommonShipmentItemsModel(models.Model):
    """
    Individual items within a shipment, linked to CommonStocksModel.
    """
    owner=models.ForeignKey(User,related_name="shipment_items_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="shipment_items_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="shipment_items_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="shipment_items_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="shipment_items_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    shipment=models.ForeignKey(CommonShipmentsModel,blank=True,null=True, on_delete=models.CASCADE, related_name='items')
    stock_item=models.ForeignKey(CommonStocksModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipment_occurrences')
    quantity=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    unit_of_measure = models.CharField(max_length=50, blank=True, null=True)
    # You might add fields like actual_weight_kg, actual_volume_cbm per item
    # unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # For costing/billing
    # total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    

    def __str__(self):
        return f"{self.quantity} {self.unit_of_measure} of {self.stock_item.item_name} in Shipment #{self.shipment.shipment_number} ({self.company.company})"


class CommonRoutesModel(models.Model):
    """
    Defines common transportation routes.
    """
    owner=models.ForeignKey(User,related_name="transport_routes_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="transport_routes_company",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="transport_routes_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="transport_routes_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="transport_routes_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    name=models.CharField(max_length=255,blank=True,null=True)
    origin_location = models.CharField(max_length=255,blank=True,null=True)
    destination_location = models.CharField(max_length=255,blank=True,null=True)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estimated_time_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True,blank=True,null=True)

    def __str__(self):
        return f"{self.name}: {self.origin_location} to {self.destination_location}"


 ##################33 contacts from the website ############3       
class CommonContactsModel(models.Model):
    name=models.CharField(max_length=50,blank=False,null=True,default="name")
    subject=models.CharField(max_length=50,blank=False,null=True,default="subject")
    email=models.EmailField(max_length=50,blank=False,null=True,default="email")
    message=models.CharField(max_length=255,blank=False,null=True,default="message")
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return str(self.subject)










########################## consider deletting eblow models ################

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
    