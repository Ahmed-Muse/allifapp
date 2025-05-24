from django.db import models
from django.template.defaultfilters import register, slugify
from uuid import uuid4 
#from django.contrib.auth.models import User
from allifmaalusersapp.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse

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

gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Organization', 'Organization'),
	)

entity_status=(
    ('Blocked', 'Entity Blocked'),
    ('Unblocked', 'Entity Unblocked'),
   
	)

  # these values should not be changed because they are hard-coded in some areas of the system
rights= [
    ('admin', 'admin'),
    ('staff', 'staff'),
    ('owner', 'owner'),
    ('guest', 'guest'),
    ('manager', 'manager'),
    ('director','director'),
	]
posting_status = [
    ('waiting','waiting'),
    ('posted', 'posted'),
    ]
delete_status= [
    ('undeletable','undeletable'),
    ('deletable', 'deletable'),
    ]
asset_current_status = [
     ('In Procurement', 'In Procurement'),
     ('In Storage', 'In Storage'),
    ('In Use','In Use'),
    ('Expired', 'Expired'),
    ('Lost', 'Lost'),
    ('Stolen', 'Stolen'),
    ('Unknown', 'Unknown'),
    ]
depreciation_method = [
    ('Straight-Line','Straight Line'),
    ('Declining-Balance', 'Declining Balance'),
    ('Double-Declining-Balance', 'Double Declining Balance'),
    ('Sum-of-the-Years-Digits', 'Sum of the Years Digits'),
    ]
payment_destination= [
    ('inbound','inbound'),
    ('outbound', 'outbound'),
    ]
source_of_funds= [
    ('Operations','Operations'),
    ('Investment', 'Investment'),
    ]
chart_of_account_statement_type= [
    ('Balance Sheet','Balance Sheet'),
    ('Income Statement', 'Income Statement'),
    ]
taxoptions = [
    ('Default', 'Default'),
     ('Dynamic', 'Dynamic'),
   
    ]



ledgerentryowner= [
    ('supplier','supplier'),
    ('customer', 'customer'),
    ('staff', 'staff'),
   
    ]

prospects = [
    ('Default', 'Default'),
    ('Likely', 'Likely'),
    ('Confirmed', 'Confirmed'),
    ('Closed', 'Closed'),
    ('Lost', 'Lost'),
   
    ]
givediscount = [
    ('Yes','Yes'),
    ('No', 'No'),
   
    ]
invoiceStatus = [
    ('Paid', 'Paid'),
    ('Current', 'Current'),
    ('Overdue', 'Overdue'),
   
    ]
  
task_status = [
    ('complete', 'complete'),
    ('incomplete', 'incomplete'),
    
    ]
day = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
    
    ]
      
job_status=[
        ("open","open"),
        ("completed","completed"),
    ]

# check lenght, ondelete, true/false
class CommonSectorsModel(models.Model):# this is the company  hospitality logistics
    name=models.CharField(max_length=30,blank=False,null=False,unique=True,default="Sector Name")
    notes=models.CharField(max_length=50,blank=True,null=True,default="Sector Comments")
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name="secownr")
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
    company=models.CharField(max_length=50,blank=True,null=True)
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
    balance=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
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
    gender=models.CharField(max_length=25, blank=True, null=True,choices=gender)

     #..... start.... below fields is special for healthcare entities setup....
    age=models.CharField(null=True, blank=True, max_length=30)
    nextkin=models.CharField(null=True, blank=True, max_length=30)
    relationship=models.CharField(null=True, blank=True, max_length=30)
    paymentType=models.ForeignKey(CommonPaymentTermsModel, related_name="custmerrpymntrms",on_delete=models.SET_NULL,null=True,blank=True)
    #..... end.... below fields is special for healthcare entities setup....

    #..... start.... below fields is special for educational setup....
    form=models.ForeignKey(CommonFormsModel,on_delete=models.SET_NULL,blank=True,null=True)
    className=models.ForeignKey(CommonClassesModel,on_delete=models.SET_NULL,blank=True,null=True)
     #..... end.... below fields is special for educational setup....
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    comments=models.CharField(null=True, blank=True, max_length=50)
    country=models.CharField(null=True, blank=True, max_length=50)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvscustmrs",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchcustmrs",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptcustmrs",on_delete=models.SET_NULL,null=True,blank=True)

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
    
################################3assets######################################################

class CommonAssetCategoriesModel(models.Model):
    description=models.CharField(max_length=30,blank=False,null=True,unique=False)
    owner=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="asstcatusr",null=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpasstcatasst",on_delete=models.CASCADE,null=True,blank=True)
    comments=models.CharField(null=True, blank=False, max_length=50)
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
    employee=models.ForeignKey(CommonEmployeesModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='asstemply')
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsassts",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchassts",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptassts",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return str(self.description)
    @property
    def asset_total_amount(self):
        assetamount=self.quantity*self.value
        return assetamount
        
class CommonExpensesModel(models.Model):
    owner=models.ForeignKey(User, related_name="cmnurexpns",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmnexpcmpn",on_delete=models.CASCADE,null=True,blank=True)
    funding_account=models.ForeignKey(CommonChartofAccountsModel, blank=False,null=True,on_delete=models.SET_NULL,related_name='coaexprelnanemconcmm')
    expense_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True, on_delete=models.SET_NULL,related_name='coaexprelnamepaytocmm')
    supplier=models.ForeignKey(CommonSuppliersModel, blank=False, null=True, on_delete=models.SET_NULL,related_name='expsupprelanmeconcmm')
    mode=models.ForeignKey(CommonPaymentTermsModel, related_name="expnspymnterms",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    description=models.CharField(max_length=50,blank=False,null=True)
    amount=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    comments=models.CharField(max_length=30,blank=True,null=True)
    status=models.CharField(choices=posting_status, default='waiting', max_length=20,blank=True,null=True)
    quantity=models.DecimalField(max_digits=30,blank=False,null=True,decimal_places=1,default=0)
    equity_account=models.ForeignKey(CommonChartofAccountsModel, blank=False, null=True, on_delete=models.SET_NULL,related_name='coexprln')
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsexpns",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchexpns",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptexpns",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return str(self.description)
    #def save(self, *args, **kwargs):
        #if self.pay_from is None:
        #self.pay_from== AllifmaalChartOfAccountsModel.objects.filter(description="Cash")
       
       
        #super(AllifmaalExpensesModel, self).save(*args, **kwargs)


#########################################3 STOCK ##############################################
class CommonStockCategoriesModel(models.Model):
    description=models.CharField(max_length=30, blank=False, null=True)
    owner=models.ForeignKey(User, related_name="cmnurstkcat",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmnstcatrln",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsstockcats",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchstockcats",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptstockcats",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    comments=models.CharField(null=True, blank=True, max_length=50)
    def __str__(self):
    		return str(self.description) # this will show up in the admin area

class CommonStocksModel(models.Model):
    category=models.ForeignKey(CommonStockCategoriesModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='catinvtconrlnm')
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
    def __str__(self):
    		return str(self.description) # this will show up in the admin area

##################################

class CommonPurchaseOrdersModel(models.Model):
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
    
class CommonContactsModel(models.Model):
    name=models.CharField(max_length=50,blank=False,null=True,default="name")
    subject=models.CharField(max_length=50,blank=False,null=True,default="subject")
    email=models.EmailField(max_length=50,blank=False,null=True,default="email")
    message=models.CharField(max_length=255,blank=False,null=True,default="message")
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return str(self.subject)

