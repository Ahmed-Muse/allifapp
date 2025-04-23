from django.urls import path
from . import views
app_name='allifmaalcommonapp'
urlpatterns = [

############################ The decision maker ##################################3
path('', views.commonWebsite, name="commonWebsite"),
path('Engineering/', views.commonEngineering, name="commonEngineering"),
path('Decision/Making/Point/', views.CommonDecisionPoint, name="CommonDecisionPoint"),
path('Home/<str:allifusr>/<str:allifslug>/', views.commonHome, name="commonHome"),

############################ Sectors ##################################3
path('Sectors/<str:allifusr>/<str:allifslug>/', views.commonSectors, name="commonSectors"),
path('Edit/Sector/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditSector, name="commonEditSector"),
path('Want/To/Delete/Sector/<str:pk>/<str:allifusr>/<str:allifslug>/Permanently/', views.commonWantToDeleteSector, name="commonWantToDeleteSector"),
path('Delete/Sector/<str:pk>/Permanently/', views.commonSectorDelete, name="commonSectorDelete"),
path('Sector/Information/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonSectorDetails, name="commonSectorDetails"),

############ testing only ...used...dont remove....#############3
path('load/new/content/in/page/', views.commonLoadContentTest, name="commonLoadContentTest"),

##################################3 DOCUMENTS FORMAT ############################
path('Allifmaal/ERP/System/Common/Modules/App/Documents/Format/<str:allifusr>/<str:allifslug>/', views.commonDocsFormat, name="commonDocsFormat"),
path('Allifmaal/ERP/System/Common/Modules/App/Edit/Document/Format/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditDocsFormat, name="commonEditDocsFormat"),
path('Allifmaal/ERP/System/Common/Modules/App/Delete/Document/Format/<str:pk>/Permanently/', views.commonDeleteDocsFormat, name="commonDeleteDocsFormat"),

################################## DATA SORTS ##############
path('Data/Sorts/<str:allifusr>/<str:allifslug>/', views.commonDataSorts, name="commonDataSorts"),
path('Edit/Data/Filter/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditDataSort, name="commonEditDataSort"),
path('Delete/Data/Filter/<str:pk>/Permanently/', views.commonDeleteDataSort, name="commonDeleteDataSort"),

############################ Entities ##################################3
path('Companies/<str:allifusr>/<str:allifslug>/', views.commonCompanies, name="commonCompanies"),
path('Company/Settings/Details/For/Subscribers/<str:allifusr>/<str:allifslug>/', views.commonCompanyDetailsForClients, name="commonCompanyDetailsForClients"),
path('Add/New/Entity/<str:allifusr>/', views.commonAddnewEntity, name="commonAddnewEntity"),
path('Edit/Entity/Details/By/Allifmaal/Admin/<slug:allifpk>/<str:allifusr>/<str:allifslug>/', views.commonEditEntityByAllifAdmin, name="commonEditEntityByAllifAdmin"),
path('Edit/Entity/Details/By/Owners/<slug:allifpk>/<str:allifusr>/<str:allifslug>/Clients/Subscribers/', views.commonEditEntityByClients, name="commonEditEntityByClients"),
path('Company/Details/For/Allifmaal/Admin/<str:pk>/<str:allifusr>/<str:allifslug>/Only/', views.commonCompanyDetailsForAllifAdmin, name="commonCompanyDetailsForAllifAdmin"),
path('Delete/Entity/<str:allifslug>/', views.commonDeleteEntity, name="commonDeleteEntity"),
path('Search/Results/<str:allifusr>/<str:allifslug>/', views.commonCompanySearch, name="commonCompanySearch"),
path('Advanced/Search/Results/<str:allifusr>/<str:allifslug>/', views.commonCompanyAdvanceSearch, name="commonCompanyAdvanceSearch"),
path('Viewing/Company/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Row/', views.commonShowClickedRowCompanyDetails, name="commonShowClickedRowCompanyDetails"),
path('Want/To/Delete/Entity/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteCompany, name="commonWantToDeleteCompany"),

########################3 company scopes ###################
path('Company/Scopes/<str:allifusr>/<str:allifslug>/', views.commonAddCompanyScope, name="commonAddCompanyScope"),
path('Edit/Company/Scope/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditCompanyScope, name="commonEditCompanyScope"),
path('Delete/Company/Scope/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteCompanyScope, name="commonDeleteCompanyScope"),
path('Want/To/Delete/This/Scope/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteScope, name="commonWantToDeleteScope"),

#########################33 branches ########################
path('Company/Divisions/<str:allifusr>/<str:allifslug>/', views.commonDivisions, name="commonDivisions"),
path('Add/New/Company/Divisions/<str:allifusr>/<str:allifslug>/', views.commonAddDivision, name="commonAddDivision"),

path('Edit/Division/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditDivision, name="commonEditDivision"),
path('Division/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDivisionDetails, name="commonDivisionDetails"),
path('Want/To/Delete/Division/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteDivision, name="commonWantToDeleteDivision"),
path('Delete/Division/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteDivision, name="commonDeleteDivision"),

#########################33 branches ########################
path('Company/Branches/<str:allifusr>/<str:allifslug>/', views.commonBranches, name="commonBranches"),
path('Add/New/Company/Branch/<str:allifusr>/<str:allifslug>/', views.commonAddBranch, name="commonAddBranch"),
path('Edit/Branch/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditBranch, name="commonEditBranch"),
path('Branch/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonBranchDetails, name="commonBranchDetails"),
path('Want/To/Delete/Branch/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteBranch, name="commonWantToDeleteBranch"),
path('Delete/Branch/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteBranch, name="commonDeleteBranch"),
path('Search/For/Branch/<str:allifusr>/<str:allifslug>/', views.commonBranchSearch, name="commonBranchSearch"),

####################3 company departments #################
path('Departments/<str:allifusr>/<str:allifslug>/', views.commonDepartments, name="commonDepartments"),
path('Add/New/Department/<str:allifusr>/<str:allifslug>/', views.commonAddDepartment, name="commonAddDepartment"),
path('Edit/Department/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Update/', views.commonEditDepartment, name="commonEditDepartment"),
path('View/Department/<str:allifslug>/<str:allifusr>/<str:allifrandom>/Details/', views.commonDepartmentDetails, name="commonDepartmentDetails"),
path('Delete/Department/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteDepartment, name="commonDeleteDepartment"),
path('Search/Departments/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonDepartmentSearch, name="commonDepartmentSearch"),
path('Want/To/Delete/Department/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteDepartment, name="commonWantToDeleteDepartment"),

############################ HRM ##################################3
path('HRM/<str:allifusr>/<str:allifslug>/', views.commonhrm, name="commonhrm"),
path('Add/New/Staff/User/<str:allifusr>/<str:allifslug>/', views.commonAddUser, name="commonAddUser"),
path('Logged/In/User/Details/<str:allifusr>/<str:allifslug>/Show/Info/', views.commonLoggedInUserDetails, name="commonLoggedInUserDetails"),

path('View/User/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonUserDetails, name="commonUserDetails"),
path('Viewing/User/Instant/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Row/', views.commonShowClickedRowUserDetails, name="commonShowClickedRowUserDetails"),
path('Update/User/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Edit/', views.commonEditUser, name="commonEditUser"),
path('Want/Tp/Delete/User/<str:pk>/<str:allifusr>/<str:allifslug>/Permanently/', views.commonWantToDeleteUser, name="commonWantToDeleteUser"),
path('Delete/User/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteUser, name="commonDeleteUser"),
path('Search/For/Employee/HRM/Staff/Details/<str:allifusr>/<str:allifslug>/', views.commonUserSearch, name="commonUserSearch"),
path('User/Can/Add/Edit/View/Delete/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonUserCanAddEditViewDelete, name="commonUserCanAddEditViewDelete"),
path('User/Can/Add/Only/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonUserCanAdd, name="commonUserCanAdd"),
path('User/Can/View/Only/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonUserCanView, name="commonUserCanView"),
path('User/Can/Edit/Only/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonUserCanEdit, name="commonUserCanEdit"),
path('User/Can/Delete/Only/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonUserCanDelete, name="commonUserCanDelete"),
path('User/Can/Access/All/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonUserCanAccessAll, name="commonUserCanAccessAll"),
path('User/Can/Access/Only/Related/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonUserCanAccessRelated, name="commonUserCanAccessRelated"),
path('User/Is/Allifmaal/Admin/<str:pk>/', views.commonUserAllifaamlAdmin, name="commonUserAllifaamlAdmin"),

############################ staff profiles ##################################3
path('Staff/Profiles/<str:allifusr>/<str:allifslug>/Main/List/', views.commonStaffProfiles, name="commonStaffProfiles"),
path('Add/New/Staff/Profile/Details/<str:allifusr>/<str:allifslug>/', views.commonAddStaffProfile, name="commonAddStaffProfile"),
path('Edit/Staff/Profile/Details/<int:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditStaffProfile, name="commonEditStaffProfile"),
path('View/Employee/Profile/Details/<str:allifslug>/<str:allifusr>/<str:allifslugstaff>/', views.commonStaffProfileDetails, name="commonStaffProfileDetails"),
path('Delete/Profile/<str:pk>/<str:allifusr>/<str:allifslug>/Permanently/', views.commonDeleteProfile, name="commonDeleteProfile"),
path('Want/Tp/Delete/Profile/<str:pk>/<str:allifusr>/<str:allifslug>/Permanently/', views.commonWantToDeleteProfile, name="commonWantToDeleteProfile"),
path('Search/For/Employee/Profile/Details/HRM/Staff/Details/<str:allifusr>/<str:allifslug>/', views.commonProfileSearch, name="commonProfileSearch"),

################################### TAXES #########################3
path('Tax/Parameters/<str:allifusr>/<str:allifslug>/', views.commonTaxParameters, name="commonTaxParameters"),
path('Update/Tax/Parameter/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.CommonUpdateTaxDetails, name="CommonUpdateTaxDetails"),
path('Delete/Tax/Parameter/<str:pk>/<str:allifusr>/<str:allifslug>/', views.CommonDeleteTaxParameter, name="CommonDeleteTaxParameter"),
path('Want/To/Delete/This/Tax/Parameter/Now/Prmntly/<str:pk>/<str:allifusr>/<str:allifslug>/Permanently/', views.commonWantToDeleteTaxParameter, name="commonWantToDeleteTaxParameter"),


##################################### General Ledger accounts ################
path('General/Ledgers/Accounts/<str:allifusr>/<str:allifslug>/', views.commonGeneralLedgers, name="commonGeneralLedgers"),
path('Add/General/Ledger/Account/<str:allifusr>/<str:allifslug>/', views.commonAddGeneralLedger, name="commonAddGeneralLedger"),
path('Edit/General/Ledger/Account/<str:allifusr>/<str:pk>/<str:allifslug>/Update/', views.commonEditGeneralLedger, name="commonEditGeneralLedger"),
path('View/General/Ledger/<str:allifslug>/<str:allifusr>/<str:allifrandom>/Details/', views.commonGeneralLedgerDetails, name="commonGeneralLedgerDetails"),
path('Delete/General/Ledger/Account/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteGeneralLedger, name="commonDeleteGeneralLedger"),
path('Synchornize/General/Ledger/Account/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonSynchGLAccount, name="commonSynchGLAccount"),
path('Want/To/Delete/General/Ledger/Account/<str:pk>/<str:allifusr>/<str:allifslug>/Permanently/', views.commonWantToDeleteGenLedger, name="commonWantToDeleteGenLedger"),

#################################3 Chart of accounts #######################
path('Chart/of/Accounts/<str:allifusr>/<str:allifslug>/', views.commonChartofAccounts, name="commonChartofAccounts"),
path('Add/Chart/of/Account/<str:allifusr>/<str:allifslug>/', views.commonAddChartofAccount, name="commonAddChartofAccount"),
path('Edit/Chart/of/Account/<str:pk>/<str:allifusr>/<str:allifslug>/Update/', views.commonEditChartofAccount, name="commonEditChartofAccount"),
path('Search/Chart/of/Accounts/<str:allifusr>/<str:allifslug>/', views.commonChartofAccountSearch, name="commonChartofAccountSearch"),
path('Chart/of/Account/<str:allifslug>/<str:allifusr>/<str:allifslugcmon>/Details/', views.commonChartofAccountDetails, name="commonChartofAccountDetails"),
path('Delete/Chart/of/Account/<str:pk>/Update/', views.commonDeleteChartofAccount, name="commonDeleteChartofAccount"),
path('Chart/of/Accounts/', views.commonSelectedRelatedAccs, name="commonSelectedRelatedAccs"),
path('Clear/Account/Balances/<str:pk>/', views.commonClearAcc, name="commonClearAcc"),
path('Want/To/Delete/Chart/of/Account/<str:pk>/<str:allifusr>/<str:allifslug>/Permanently/', views.commonWantToDeleteCoA, name="commonWantToDeleteCoA"),
path('Chart/of/Accounts/Advanced/Search/<str:allifusr>/<str:allifslug>/', views.commonChartofAccAdvanceSearch, name="commonChartofAccAdvanceSearch"),

#################################3 EMAILS AND SMSs ####################
path('Emails/And/SMSs/<str:allifusr>/<str:allifslug>/', views.commonEmailsAndSMS, name="commonEmailsAndSMS"),
path('Delete/Bank/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteEmail, name="commonDeleteEmail"),

###############################3 BANKS ##############
path('Banks/<str:allifusr>/<str:allifslug>/', views.commonBanks, name="commonBanks"),
path('Add/New/Bank/<str:allifusr>/<str:allifslug>/', views.commonAddBank, name="commonAddBank"),
path('Edit/Bank/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Update/', views.commonEditBank, name="commonEditBank"),
path('View/Bank/<str:allifslug>/<str:allifusr>/<str:allifrandom>/Details/', views.commonBankDetails, name="commonBankDetails"),
path('Delete/Bank/<str:pk>/<str:allifusr>/<str:allifslug>/Permntly/', views.commonDeleteBank, name="commonDeleteBank"),
path('Search/Bank/<str:allifusr>/<str:allifslug>/', views.commonBankSearch, name="commonBankSearch"),
path('Want/To/Delete/Bank/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteBank, name="commonWantToDeleteBank"),

#####################################3 BANK OPERATIONS ###################################
path('Bank/Deposits/<str:allifusr>/<str:allifslug>/', views.commonBankShareholderDeposits, name="commonBankShareholderDeposits"),
path('Add/New/Bank/Deposit/<str:allifusr>/<str:allifslug>/', views.commonAddBankShareholderDeposit, name="commonAddBankShareholderDeposit"),
path('Edit/Bank/Deposit/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditBankShareholderDeposit, name="commonEditBankShareholderDeposit"),
path('Bank/Deposit/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonBankShareholderDepositDetails, name="commonBankShareholderDepositDetails"),
path('Delete/Bank/Deposit/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteBankShareholderDeposit, name="commonDeleteBankShareholderDeposit"),
path('Search/Bank/Deposit/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonDepositSearch, name="commonDepositSearch"),
path('Want/To/Delete/Deposit/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteDeposit, name="commonWantToDeleteDeposit"),
path('Search/Results/Deposits/<str:allifusr>/<str:allifslug>/', views.commonDepositAdvanceSearch, name="commonDepositAdvanceSearch"),
path('Clear/Shareholder/Search/Results/Deposits/<str:allifusr>/<str:allifslug>/', views.commonClearShareholderDepositSearch, name="commonClearShareholderDepositSearch"),

####################################3 withdrawals ###########################3
path('Bank/Withdrawals/<str:allifusr>/<str:allifslug>/', views.commonBankWithdrawals, name="commonBankWithdrawals"),
path('Add/New/Bank/Withdrawal/<str:allifusr>/<str:allifslug>/', views.commonAddBankWithdrawal, name="commonAddBankWithdrawal"),
path('Edit/Bank/Withdrawal/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditBankWithdrawal, name="commonEditBankWithdrawal"),
path('Bank/Withdrawal/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonBankWithdrawalDetails, name="commonBankWithdrawalDetails"),
path('Delete/Bank/Withdrawal/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteBankWithdrawal, name="commonDeleteBankWithdrawal"),
path('Search/Bank/Withdrawals/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonWithdrawalSearch, name="commonWithdrawalSearch"),
path('Want/To/Delete/Withdrawal/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteWithdrawal, name="commonWantToDeleteWithdrawal"),
path('Search/Results/Withdrawals/<str:allifusr>/<str:allifslug>/', views.commonWithdrawalAdvanceSearch, name="commonWithdrawalAdvanceSearch"),
path('Clear/Shareholder/Search/Results/Withdrawls/<str:allifusr>/<str:allifslug>/', views.commonClearShareholderWithdrwlSearch, name="commonClearShareholderWithdrwlSearch"),

############################ suppliers sections ##################################3
path('Suppliers/<str:allifusr>/<str:allifslug>/List/', views.commonSuppliers, name="commonSuppliers"),
path('Add/Supplier/<str:allifusr>/<str:allifslug>/New/', views.commonAddSupplier, name="commonAddSupplier"),
path('Edit/Supplier/<str:pk>/<str:allifusr>/<str:allifslug>/Update/', views.commonEditSupplier, name="commonEditSupplier"),
path('View/Supplier/<str:allifslug>/<str:allifusr>/<str:allifslugrandom>/Details/', views.commonSupplierDetails, name="commonSupplierDetails"),
path('Delete/Supplier/<str:pk>/<str:allifusr>/<str:allifslug>/Permntly/', views.commonDeleteSupplier, name="commonDeleteSupplier"),
path('Search/Suppliers/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonSupplierSearch, name="commonSupplierSearch"),
path('Want/To/Delete/Supplier/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteSupplier, name="commonWantToDeleteSupplier"),
path('Search/Results/Suppliers/<str:allifusr>/<str:allifslug>/', views.commonSupplierAdvanceSearch, name="commonSupplierAdvanceSearch"),
path('Clear/Suplier/Search/Results/Deposits/<str:allifusr>/<str:allifslug>/', views.commonClearSupplierSearch, name="commonClearSupplierSearch"),

 ############################3 CUSTOMERS SECTION ################################### 
path('Forms/<str:allifusr>/<str:allifslug>/', views.commonForms, name="commonForms"),
path('Add/New/Form/<str:allifusr>/<str:allifslug>/', views.commonAddForm, name="commonAddForm"),
path('Edit/Form/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditForm, name="commonEditForm"),
path('Delete/Form/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteForm, name="commonDeleteForm"),
path('View/Form/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonFormDetails, name="commonFormDetails"),
path('Search/Forms/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonFormSearch, name="commonFormSearch"),
path('Want/To/Delete/Form/Faculty/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteForm, name="commonWantToDeleteForm"),

################################3333 classes #########################################################
path('Classes/<str:allifusr>/<str:allifslug>/', views.commonClasses, name="commonClasses"),
path('Add/New/Class/<str:allifusr>/<str:allifslug>/', views.commonAddClass, name="commonAddClass"),
path('Edit/Class/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditClass, name="commonEditClass"),
path('Delete/Class/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteClass, name="commonDeleteClass"),
path('Search/Classes/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonClassSearch, name="commonClassSearch"),
path('View/Class/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonClassDetails, name="commonClassDetails"),
path('Want/To/Delete/This/Class/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteClass, name="commonWantToDeleteClass"),

###################################### Customers ##########################################################
path('Customers/<str:allifusr>/<str:allifslug>/', views.commonCustomers, name="commonCustomers"),
path('Add/Customers/<str:allifusr>/<str:allifslug>/', views.commonAddCustomer, name="commonAddCustomer"),
path('Edit/Record/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonEditCustomer, name="commonEditCustomer"),
path('View/Record/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonCustomerDetails, name="commonCustomerDetails"),
path('Delete/Record/<str:pk>/<str:allifusr>/<str:allifslug>/Details/Permntly/', views.commonDeleteCustomer, name="commonDeleteCustomer"),
path('Search/Customers/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonCustomerSearch, name="commonCustomerSearch"),
path('Search/Results/Customers/<str:allifusr>/<str:allifslug>/', views.commonCustomerAdvanceSearch, name="commonCustomerAdvanceSearch"),
path('Want/To/Delete/This/Customer/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteCustomer, name="commonWantToDeleteCustomer"),

################################ assets #######################

#####################3 company departments #################
path('Assets/Categories/<str:allifusr>/<str:allifslug>/', views.commonAssetCategories, name="commonAssetCategories"),
path('Add/New/Asset/Category/<str:allifusr>/<str:allifslug>/', views.commonAddAssetCategory, name="commonAddAssetCategory"),
path('Edit/Asset/Category/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Update/', views.commonEditAssetCategory, name="commonEditAssetCategory"),
path('View/Asset/Category/<str:allifslug>/<str:allifusr>/<str:allifrandom>/Details/', views.commonAssetCategoryDetails, name="commonAssetCategoryDetails"),
path('Delete/Asset/Category/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteAssetCategory, name="commonDeleteAssetCategory"),
path('Search/Asset/Category/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonAssetCategorySearch, name="commonAssetCategorySearch"),
path('Want/To/Delete/This/Asset/Category/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteAssetCategory, name="commonWantToDeleteAssetCategory"),

##############################3############# Main Assets #############################################
path('Assets/<str:allifusr>/<str:allifslug>/', views.commonAssets, name="commonAssets"),
path('Add/Asset/<str:allifusr>/<str:allifslug>/New/', views.commonAddAsset, name="commonAddAsset"),
path('Edit/Asset/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonEditAsset, name="commonEditAsset"),
path('Asset/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonAssetDetails, name="commonAssetDetails"),
path('Delete/Asset/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonDeleteAsset, name="commonDeleteAsset"),
path('Search/Asset/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonAssetSearch, name="commonAssetSearch"),
path('Post/Asset/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonPostAsset, name="commonPostAsset"),
path('Want/To/Delete/This/Asset/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteAsset, name="commonWantToDeleteAsset"),

################################### ASSET DEPRECATION ############33
path('Depreciate/Asset/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonDepreciateAsset, name="commonDepreciateAsset"),

############################33 expenses ####################################################
path('Expenses/<str:allifusr>/<str:allifslug>/', views.commonExpenses, name="commonExpenses"),
path('Add/New/Expense/<str:allifusr>/<str:allifslug>/', views.commonAddExpense, name="commonAddExpense"),
path('Edit/Expense/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditExpense, name="commonEditExpense"),
path('Expense/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonExpenseDetails, name="commonExpenseDetails"),
path('Delete/This/Expense/?/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteExpense, name="commonWantToDeleteExpense"),
path('Delete/Expense/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteExpense, name="commonDeleteExpense"),
path('Post/Expense/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonPostExpense, name="commonPostExpense"),
path('Search/Expense/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonExpenseSearch, name="commonExpenseSearch"),

######################################## stocks ######################3
path('Stock/Categories/<str:allifusr>/<str:allifslug>/List/', views.commonStockCats, name="commonStockCats"),
path('Add/New/Stock/Category/<str:allifusr>/<str:allifslug>/List/', views.commonAddStockCat, name="commonAddStockCat"),
path('Edit/Category/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditStockCat, name="commonEditStockCat"),
path('Delete/Category/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteStockCat, name="commonDeleteStockCat"),
path('Stock/Category/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonStockCategoryDetails, name="commonStockCategoryDetails"),
path('Inventory/Stock/<str:allifusr>/<str:allifslug>/', views.commonStocks, name="commonStocks"),
path('Add/New/Stock/<str:allifusr>/<str:allifslug>/Inventory/', views.commonAddStockItem, name="commonAddStockItem"),
path('Edit/Stock/Item/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditStockItem, name="commonEditStockItem"),
path('Stock/Item/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonStockItemDetails, name="commonStockItemDetails"),
path('Delete/Stock/Item/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteStockItem, name="commonDeleteStockItem"),
path('Want/To/Delete/This/Stock/Category/Now/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteStockCat, name="commonWantToDeleteStockCat"),
path('Want/To/Delete/This/Stock/Item/Now/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteStockItem, name="commonWantToDeleteStockItem"),
path('Search/Stock/Item/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonStockItemSearch, name="commonStockItemSearch"),
path('Search/Stock/Category/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonStockCategorySearch, name="commonStockCategorySearch"),
path('Advanced/Stock/Items/Search/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonStockItemAdvanceSearch, name="commonStockItemAdvanceSearch"),

######################################3 PURCHASES ###########################################
path('Purchases/Orders/<str:allifusr>/<str:allifslug>/', views.commonPurchaseOrders, name="commonPurchaseOrders"),
path('New/Purchase/Order/<str:allifusr>/<str:allifslug>/', views.commonNewPurchaseOrder, name="commonNewPurchaseOrder"),
path('Delete/Purchase/Order/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeletePO, name="commonDeletePO"),
path('Add/Purchase/Order/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonAddPODetails, name="commonAddPODetails"),
path('Add/PO/Item/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonAddPOItems, name="commonAddPOItems"),
path('Delete/Purchase/Order/Item/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeletePOItem, name="commonDeletePOItem"),
path('Purchase/Order/Mis/Costs/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonPOMiscCost, name="commonPOMiscCost"),
path('Post/PO/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonPostPO, name="commonPostPO"),
path('PO/Misc/Cost/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonPOMiscCostDetails, name="commonPOMiscCostDetails"),
path('Delete/PO/Misc/Cost/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteMiscCost, name="commonDeleteMiscCost"),
path('Edit/PO/Misc/Cost/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditPOMiscCostDetails, name="commonEditPOMiscCostDetails"),
path('Convert/PO/PDF/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonPOToPdf, name="commonPOToPdf"),
path('Advanced/Stock/Purchase/Orders/Search/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonPOAdvanceSearch, name="commonPOAdvanceSearch"),
path('Search/Purchase/Orders/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonPOSearch, name="commonPOSearch"),
path('Want/To/Delete/Ths/Purchase/Order/Now/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeletePO, name="commonWantToDeletePO"),
path('Want/To/Delete/This/Purchase/Order/Item/Now/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeletePOItem, name="commonWantToDeletePOItem"),
path('Edit/Purchase/Order/Item/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditPOItem, name="commonEditPOItem"),
path('Calculate/Purchase/Order/s/Misc/Costs/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonCalculatePOMiscCosts, name="commonCalculatePOMiscCosts"),

################################### QUOTATIONS #######################################
path('Quotes/<str:allifusr>/<str:allifslug>/', views.commonQuotes, name="commonQuotes"),
path('New/Quote/<str:allifusr>/<str:allifslug>/', views.commonNewQuote, name="commonNewQuote"),
path('Delete/Quote/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteQuote, name="commonDeleteQuote"),
path('Add/Quote/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonAddQuoteDetails, name="commonAddQuoteDetails"),
path('Add/Quote/Items/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonAddQuoteItems, name="commonAddQuoteItems"),
path('Delete/Quote/Item/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteQuoteItem, name="commonDeleteQuoteItem"),
path('Convert/Quote/To/Pdf/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonQuoteToPdf, name="commonQuoteToPdf"),
path('Search/For/Quotes/<str:allifusr>/<str:allifslug>/', views.commonSearchAjaxQuote, name="commonSearchAjaxQuote"),
path('Search/For/Quotes/Quotations/<str:allifusr>/<str:allifslug>/', views.commonQuotesSearch, name="commonQuotesSearch"),
path('Advanced/Quotations/Search/<str:allifusr>/<str:allifslug>/', views.commonQuoteAdvanceSearch, name="commonQuoteAdvanceSearch"),
path('Want/To/Delete/This/Quotation/Permntly/Now/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteQuote, name="commonWantToDeleteQuote"),
path('Want/To/Delete/This/Quote/Item/Permntly/Now/<str:pk>/<str:allifusr>/<str:allifslug>/Now/', views.commonWantToDeleteQuoteItem, name="commonWantToDeleteQuoteItem"),
path('Edit/Quote/Item/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Now/', views.commonEditQuoteItem, name="commonEditQuoteItem"),

####################################### INVOICES ##################################
path('Invoices/<str:allifusr>/<str:allifslug>/', views.commonInvoices, name="commonInvoices"),
path('New/Invoice/<str:allifusr>/<str:allifslug>/', views.commonNewInvoice, name="commonNewInvoice"),
path('Delete/Invoice/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteInvoice, name="commonDeleteInvoice"),
path('Add/Invoice/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonAddInvoiceDetails, name="commonAddInvoiceDetails"),
path('Add/Invoice/Items/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonAddInvoiceItems, name="commonAddInvoiceItems"),
path('Delete/Invoice/Item/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteInvoiceItem, name="commonDeleteInvoiceItem"),
path('Post/Invoice/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonPostInvoice, name="commonPostInvoice"),
path('Posted/Invoices/<str:allifusr>/<str:allifslug>/', views.commonPostedInvoices, name="commonPostedInvoices"),
path('Invoice/To/Pdf/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonInvoiceToPdf, name="commonInvoiceToPdf"),
path('Search/For/Invoices/<str:allifusr>/<str:allifslug>/', views.commonSearchAjaxInvoice, name="commonSearchAjaxInvoice"),
path('Search/For/Invoices//<str:allifusr>/<str:allifslug>/', views.commonInvoicesSearch, name="commonInvoicesSearch"),
path('Advanced/Invoices/Search/<str:allifusr>/<str:allifslug>/List/Invoices/', views.commonInvoiceAdvanceSearch, name="commonInvoiceAdvanceSearch"),
path('Want/To/Delete/This/Invoice/Permntly/Now/<str:pk>/<str:allifusr>/<str:allifslug>/Now/', views.commonWantToDeleteInvoice, name="commonWantToDeleteInvoice"),
path('Want/To/Delete/This/Invoice/Item/Permntly/Now/<str:pk>/<str:allifusr>/<str:allifslug>/Now/From/Invoice/', views.commonWantToDeleteInvoiceItem, name="commonWantToDeleteInvoiceItem"),
path('Edit/Invoice/Item/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Now/For/This/Invoice/', views.commonEditInvoiceItem, name="commonEditInvoiceItem"),

#################### Supplier Ledger Entries ##############
path('Ledger/Entries/Common/<str:allifusr>/<str:allifslug>/', views.commonLedgerEntries, name="commonLedgerEntries"),
path('Ledger/Entry/General/Information/Viewing/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Now/ledg/details/', views.commonLedgerEntryDetails, name="commonLedgerEntryDetails"),
path('Want/To/Delete/This/Ledger/Entry/Permntly/Now/For/Sure/<str:pk>/<str:allifusr>/<str:allifslug>/Now/', views.commonWantToDeleteLedgerEntry, name="commonWantToDeleteLedgerEntry"),
path('Delete/This/Ledger/Entry/Permntly/Now/<str:pk>/<str:allifusr>/<str:allifslug>/Now/', views.commonDeleteLedgerEntry, name="commonDeleteLedgerEntry"),
path('Common/Search/For/Ledger/Entries/Details/<str:allifusr>/<str:allifslug>/', views.commonLedgerEntrySearch, name="commonLedgerEntrySearch"),
path('Advanced/Search/For/Ledger/Entries/Details/<str:allifusr>/<str:allifslug>/', views.commonLedgerEntryAdvanceSearch, name="commonLedgerEntryAdvanceSearch"),
path('Supplier/Ledger/Entries/Viewing/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Now/From/Invoice/', views.commonSupplierLedgerEntries, name="commonSupplierLedgerEntries"),
path('Customer/Ledger/Entries/Viewing/Detls/<str:pk>/<str:allifusr>/<str:allifslug>/Now/From/Dtils/', views.commonCustomerLedgerEntries, name="commonCustomerLedgerEntries"),
path('Staff/Ledger/Entries/Viewing/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Now/From/Details/', views.commonStaffLedgerEntries, name="commonStaffLedgerEntries"),

########################3 supplier payments #############################
path('Supplier/Payments/<str:allifusr>/<str:allifslug>/', views.commonSupplierPayments, name="commonSupplierPayments"),
path('Supplier/Payment/Processing/<str:pk>/<str:allifusr>/<str:allifslug>/Now/', views.commonPaySupplier, name="commonPaySupplier"),
path('Delete/Supplier/Payment/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteSupplierPayment, name="commonDeleteSupplierPayment"),
path('Supplier/Payment/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonSupplierPaymentDetails, name="commonSupplierPaymentDetails"),
path('Edit/Supplier/Payment/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditSupplierPayment, name="commonEditSupplierPayment"),
path('Post/Supplier/Payment/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonPostSupplierPayment, name="commonPostSupplierPayment"),
path('Posted/Supplier/Payments/<str:allifusr>/<str:allifslug>/', views.commonPostedSupplierPayments, name="commonPostedSupplierPayments"),
path('Pay/Supplier/<str:allifusr>/<str:allifslug>/', views.commonPaySupplierDirect, name="commonPaySupplierDirect"),
path('Search/For/Supplier/Payments/From/Database/<str:allifusr>/<str:allifslug>/', views.commonSupplierPaymentSearch, name="commonSupplierPaymentSearch"),
path('Want/To/Delete/This/Supplier/Payment/Item/Permntly/Now/<str:pk>/<str:allifusr>/<str:allifslug>/Now/From/Invoice/', views.commonWantToDeleteSupplierPayment, name="commonWantToDeleteSupplierPayment"),
path('Supplier/Statement/Pdf/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonSupplierStatementpdf, name="commonSupplierStatementpdf"),
path('Advanced/Search/For/Supplier/Payment/Details/<str:allifusr>/<str:allifslug>/', views.commonSupplierPaymentAdvanceSearch, name="commonSupplierPaymentAdvanceSearch"),

######################### customer payments and statments ########################
path('Customer/Payments/<str:allifusr>/<str:allifslug>/', views.commonCustomerPayments, name="commonCustomerPayments"),
path('Customer/Payment/Processing/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonTopUpCustomerAccount, name="commonTopUpCustomerAccount"),
path('Edit/Customer/Payment/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditCustomerPayment, name="commonEditCustomerPayment"),
path('Delete/Customer/Payment/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteCustomerPayment, name="commonDeleteCustomerPayment"),
path('Customer/Payment/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonCustomerPaymentDetails, name="commonCustomerPaymentDetails"),
path('Post/Customer/Payment/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonPostCustomerPayment, name="commonPostCustomerPayment"),
path('Posted/Customer/Payments/<str:allifusr>/<str:allifslug>/', views.commonPostedCustomerPayments, name="commonPostedCustomerPayments"),
path('Receive/And/Receipt/Customer/Payment/To/Account<str:allifusr>/<str:allifslug>/', views.commonReceiveCustomerMoney, name="commonReceiveCustomerMoney"),
path('Customer/Statement/Pdf/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonCustomerStatementpdf, name="commonCustomerStatementpdf"),
path('Want/To/Delete/This/Customer/Payment/value/Permntly/Now/<str:pk>/<str:allifusr>/<str:allifslug>/Now/From/Invoice/', views.commonWantToDeleteCustomerPayment, name="commonWantToDeleteCustomerPayment"),
path('Search/For/Customer/Payment/Details/Basic/Search/<str:allifusr>/<str:allifslug>/', views.commonCustomerPaymentSearch, name="commonCustomerPaymentSearch"),
path('Advanced/Search/For/Customer/Payment/Details/<str:allifusr>/<str:allifslug>/', views.commonCustomerPaymentAdvanceSearch, name="commonCustomerPaymentAdvanceSearch"),

#########################3 staf salariess ####################
path('Staff/Salries/<str:allifusr>/<str:allifslug>/', views.commonSalaries, name="commonSalaries"),
path('Add/Salary/<str:allifusr>/<str:allifslug>/', views.commonAddSalary, name="commonAddSalary"),
path('Salary/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonSalaryDetails, name="commonSalaryDetails"),
path('Edit/Salary/Details/Now/Update/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditSalaryDetails, name="commonEditSalaryDetails"),
path('Delete/Salary/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteSalary, name="commonDeleteSalary"),
path('Post/Salary/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonPostSalary, name="commonPostSalary"),
path('Posted/Salries/<str:allifusr>/<str:allifslug>/', views.commonPostedSalaries, name="commonPostedSalaries"),
path('Search/For/Staff/Salary/Payment/Details/Basic/Search/<str:allifusr>/<str:allifslug>/', views.commonSalarySearch, name="commonSalarySearch"),
path('Advanced/Search/For/Staff/Salary/Payment/Details/<str:allifusr>/<str:allifslug>/', views.commonSalaryAdvanceSearch, name="commonSalaryAdvanceSearch"),
path('Want/To/Delete/This/Salary/Payment/value/Permntly/Now/<str:pk>/<str:allifusr>/<str:allifslug>/From/List/', views.commonWantToDeleteSalary, name="commonWantToDeleteSalary"),

##################################3 JOBS ###############################
path('Jobs/<str:allifusr>/<str:allifslug>/', views.commonJobs, name="commonJobs"),
path('Create/New/Job/<str:allifusr>/<str:allifslug>/', views.commonNewJobs, name="commonNewJobs"),
path('Delete/Job/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteJob, name="commonDeleteJob"),
path('Add/Job/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Update/', views.commonAddJobDetails, name="commonAddJobDetails"),
path('Add/Job/Items/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonAddJobItems, name="commonAddJobItems"),
path('Delete/Job/Item/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteJobItem, name="commonDeleteJobItem"),
path('Invoice/Job/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonInvoiceJob, name="commonInvoiceJob"),
path('Convert/Job/pdf/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonJobInvoicePdf, name="commonJobInvoicePdf"),
path('Job/Transactions/Report/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonJobTransactionReportpdf, name="commonJobTransactionReportpdf"),
path('Search/For/Job/Details/Basic/Search/<str:allifusr>/<str:allifslug>/', views.commonJobSearch, name="commonJobSearch"),
path('Advanced/Search/For/Jobs/Details/<str:allifusr>/<str:allifslug>/', views.commonJobAdvanceSearch, name="commonJobAdvanceSearch"),
path('Want/To/Delete/This/Job/Entry/Permntly/Now/<str:pk>/<str:allifusr>/<str:allifslug>/From/List/', views.commonWantToDeleteJob, name="commonWantToDeleteJob"),
path('Want/To/Delete/This/Job/Item/Entries/From/This/Job/Permntly/Now/<str:pk>/<str:allifusr>/<str:allifslug>/From/List/', views.commonWantToDeleteJobItem, name="commonWantToDeleteJobItem"),

#############################3 TASKS #########################
path('Tasks/<str:allifusr>/<str:allifslug>/', views.commonTasks, name="commonTasks"),
path('Complete/Task/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonMarkTaskComplete, name="commonMarkTaskComplete"),
path('Completed/Tasks/<str:allifusr>/<str:allifslug>/', views.commonCompletedTasks, name="commonCompletedTasks"),
path('Delete/Task/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteTask, name="commonDeleteTask"),
path('Edit/Task/Update/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditTask, name="commonEditTask"),
path('Search/For/Job/Details/Basic/Search/<str:allifusr>/<str:allifslug>/', views.commonTasksSearch, name="commonJobSearch"),
path('Task/Details/Basic/Search/<str:allifusr>/<str:allifslug>/', views.commonTaskBasicSearch, name="commonTaskBasicSearch"),
path('Add/See/Task/Details/View/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonAddSeeTaskDetails, name="commonAddSeeTaskDetails"),

####################################### profit and loss ######################
path('Profit/And/Loss/Analysis/<str:allifusr>/<str:allifslug>/', views.commonProfitAndLoss, name="commonProfitAndLoss"),

################################### REPORTS #####################################
path('Reports/<str:allifusr>/<str:allifslug>/', views.commonMainReports, name="commonMainReports"),
path('Debtors/Report/<str:allifusr>/<str:allifslug>/', views.commonDebtorsReport, name="commonDebtorsReport"),
path('Creditors/Report/<str:allifusr>/<str:allifslug>/', views.commonCreditorsReportpdf, name="commonCreditorsReportpdf"),
path('Available/Stock/Report/<str:allifusr>/<str:allifslug>/', views.commonAvailableStockpdf, name="commonAvailableStockpdf"),

path('Contact/Information/Saving/', views.commonCustomerContacts, name="commonCustomerContacts"),




############################3
path('Table/scroll/Horizontal<str:allifusr>/<str:allifslug>/', views.commonScrollableTable, name="commonScrollableTable"),


path('UI1/Home/<str:allifusr>/<str:allifslug>/', views.ui1, name="ui1"),

path('UI2/Home/<str:allifusr>/<str:allifslug>/', views.ui2, name="ui2"),
path('UI3/Home/<str:allifusr>/<str:allifslug>/', views.ui3, name="ui3"),
path('UI4/Home/<str:allifusr>/<str:allifslug>/', views.ui4, name="ui4"),

path('UI6/Home/<str:allifusr>/<str:allifslug>/', views.ui6, name="ui6"),
path('UI7/Home/<str:allifusr>/<str:allifslug>/', views.ui7, name="ui7"),

path('UI8/Home/<str:allifusr>/<str:allifslug>/', views.ui8, name="ui8"),

###################3 links test ############3
path('links/lists', views.link_list, name='link_list'),
path('add/new/link', views.add_link, name='add_link'),

path('add/dynamic_form_view/', views.dynamic_form_view, name='dynamic_form_view'),




]   
