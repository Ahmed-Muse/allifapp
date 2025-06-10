# healthcare_app/constants.py (or a similar location)
############ below is for teh common orders/transactions model... can be applied there....
COMMON_EVENT_TYPES = [
    ('SALES_ORDER', 'Sales Order'),
    ('PATIENT_ENCOUNTER', 'Patient Encounter (Healthcare)'),
    ('GUEST_ACCOMMODATION', 'Guest Accommodation (Hospitality)'),
    ('GUEST_FOOD_ORDER', 'Guest Food Order (Hospitality)'),
    ('STUDENT_ENROLLMENT', 'Student Enrollment (Education)'),
    ('STUDENT_PAYMENT', 'Student Payment (Education)'),
    ('COURSE_REGISTRATION', 'Course Registration (Education)'),
    ('EXAM_EVENT', 'Exam Event (Education)'),
    ('SHIPPING_MANIFEST', 'Shipping Manifest (Logistics)'),
    ('PROPERTY_LEASE_AGREEMENT', 'Property Lease Agreement (Real Estate)'),
    ('CONSULTING_SESSION', 'Consulting Session (Services)'),
    # Add more as needed for different industries, ensuring unique codes
]

# Medical Service Types
operation_year_options= [
    ('Current', 'Current'),
    ('Passed', 'Passed'),
    ('Future', 'Future'),
  
]
MEDICAL_SERVICE_TYPES = [
    ('CONS', 'Consultation'),
    ('LAB', 'Lab Test'),
    ('IMG', 'Imaging'),
    ('PROC', 'Procedure'),
    ('WARD', 'Ward Charge'),
    ('PHARM', 'Pharmacy Item'), # For direct sales in pharmacy
    ('OTH', 'Other'),
]

# Prescription Formulations
PRESCRIPTION_FORMULATIONS = [
    ('TAB', 'Tablet'),
    ('SYR', 'Syrup'),
    ('CAP', 'Capsule'),
    ('INJ', 'Injection'),
    ('CREAM', 'Cream'),
    ('DROPS', 'Drops'),
    ('OTH', 'Other'),
]

# Medication Administration Routes
ADMINISTRATION_ROUTES = [
    ('ORAL', 'Oral'),
    ('IM', 'Intramuscular Injection'),
    ('IV', 'Intravenous Injection'),
    ('INHAL', 'Inhalation'),
    ('TOPIC', 'Topical'),
    ('SUBQ', 'Subcutaneous'),
]

###########3 below defines item stock status... is it physical or service ...
item_in_physical_state_or_service = [
    ('Physical', 'Physical'),
    ('Service', 'Service'),
  
]


# Dosage Units
DOSAGE_UNITS = [
    ('MG', 'Milligrams'),
    ('G', 'Grams'),
    ('ML', 'Milliliters'),
    ('UNIT', 'Units'),
    ('PIECE', 'Pieces'),
    ('DROP', 'Drops'),
    ('MCG', 'Micrograms'),
]

# Bed Occupancy Statuses
OCCUPANCY_STATUSES = [
    ('VACANT', 'Vacant'),
    ('OCCUPIED', 'Occupied'),
    ('RESERVED', 'Reserved'),
    ('CLEANING', 'Cleaning/Maintenance'),
    ('ISOLATION', 'Isolation'),
]

# Appointment Statuses
APPOINTMENT_STATUSES = [
    ('SCH', 'Scheduled'),
    ('CON', 'Confirmed'),
    ('COMP', 'Completed'),
    ('CAN', 'Cancelled'),
    ('NS', 'No Show'),
]

# Admission Statuses
ADMISSION_STATUSES = [
    ('ADM', 'Admitted'),
    ('DIS', 'Discharged'),
    ('TRANS', 'Transferred'),
    ('AWD', 'Absconded Without Discharge'),
]

# Referral Types
REFERRAL_TYPES = [
    ('INT', 'Internal'), # Within the same hospital/clinic network
    ('EXT', 'External'), # To another organization
]

# Referral Statuses
REFERRAL_STATUSES = [
    ('PEND', 'Pending'),
    ('ACC', 'Accepted'),
    ('REJ', 'Rejected'),
    ('COMP', 'Completed'),
]

# Lab Test Statuses
LAB_TEST_STATUSES = [
    ('ORD', 'Ordered'),
    ('SCOL', 'Sample Collected'),
    ('SPROC', 'Sample Processing'),
    ('COMP', 'Completed'),
    ('VALID', 'Validated'),
    ('CANC', 'Cancelled'),
]

# Imaging Test Statuses
IMAGING_TEST_STATUSES = [
    ('ORD', 'Ordered'),
    ('SCH', 'Scheduled'),
    ('PERF', 'Performed'),
    ('REPO', 'Reported'),
    ('CANC', 'Cancelled'),
]
BED_TYPES=[
        ('STD', 'Standard'), ('PRI', 'Private'), ('SEMIP', 'Semi-Private'),
        ('ICU', 'ICU Bed'), ('NICU', 'NICU Bed')
    ]
# Patient Gender
PATIENT_GENDERS = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

# Patient Blood Groups
BLOOD_GROUPS = [
    ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
]

# Encounter Types
ENCOUNTER_TYPES = [
    ('OUTP', 'Outpatient Visit'),
    ('INPAT', 'Inpatient Admission'),
    ('EMER', 'Emergency Visit'),
    ('TELE', 'Teleconsultation'),
    ('FOLLOW', 'Follow-up Visit'),
]


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
approval_status= [
    ('pending', 'pending'),
    ('approved', 'approved'),
   
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

DrugForm = [
    ('Tablet','Tablet'),
    ('Syrub', 'Syrub'),
    ('Powder','Powder'),
    ('Liquid','Liquid')
   
    ]
DrugUnits = [
    ('Grams','Grams'),
    ('Pieces', 'Pieces'),
    ('Miligrams','Miligrams'),
    ('Mililiters','Mililiters'),
   
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

payment_status = [('PENDING', 'Pending'), ('PAID', 'Paid'), ('DUE', 'Due')]
####################3 hospitality ######################
 #Example for up to 20 floors
FLOOR_CHOICES = [(i, str(i)) for i in range(1, 21)]

CURRENT_STATUS_CHOICES = [
        ('AVAIL', 'Available'),
        ('OCC', 'Occupied'),
        ('MAINT', 'Maintenance'),
        ('DIRTY', 'Dirty'),
    ]
BOOKING_STATUS_CHOICES = [
        ('PEND', 'Pending'),
        ('CONF', 'Confirmed'),
        ('CHECKIN', 'Checked-In'),
        ('CHECKOUT', 'Checked-Out'),
        ('CANCEL', 'Cancelled'),
        ('NOSHOW', 'No Show')
    ]
STATUS_CHOICES = [
        ('AVAIL', 'Available'),
        ('OCC', 'Occupied'),
        ('RESERVED', 'Reserved'),
        ('CLEAN', 'Needs Cleaning'),
    ]
ORDER_STATUS_CHOICES = [
        ('PEND', 'Pending'),
        ('PREP', 'Preparing'),
        ('SERVED', 'Served'),
        ('COMP', 'Completed'), # Ready for billing
        ('CANCEL', 'Cancelled')
    ]

STATUS_CHOICES_STATE = [
        ('PEND', 'Pending'),
        ('PREP', 'Preparing'),
        ('READY', 'Ready for Serve'),
        ('SERVED', 'Served'),
        ('CANCEL', 'Cancelled')
    ]

####################3 education ###########3
student_status_choices = [('ENR', 'Enrolled'), ('DROP', 'Dropped'), ('COMP', 'Completed')]
day_of_week_choices = [
        ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'),
        ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')
    ]

############################ real estates #####################3

PROPERTY_TYPES = [
        ('RES', 'Residential'),
        ('COM', 'Commercial'),
        ('IND', 'Industrial'),
        ('LAND', 'Land'),
        ('MIXED', 'Mixed-Use'),
    ]
PROPERTY_UNIT_TYPES = [
        ('APT', 'Apartment'),
        ('ROOM', 'ROOM'),
        ('SHOP', 'Shop'),
        ('OFFICE', 'Office'),
        ('HOUSE', 'House'),
        ('WAREHOUSE', 'Warehouse'),
        ('OTHER', 'Other'),
    ]
PROJECT_STATUS_CHOICES=[
        ('PLAN', 'Planned'), ('INPR', 'In Progress'), ('PAUSE', 'Paused'),('SCHED', 'Scheduled'),
        ('COMP', 'Completed'), ('CANC', 'Cancelled')
    ]

 
PROPERTY_STATUS_TYPES = [
    ('SALE', 'For Sale'), ('RENT', 'For Rent'), ('DEV', 'For Development'),
     ('ACT', 'Active'), ('PEND', 'Pending'), ('SOLD', 'Sold'),
    ('RENTED', 'Rented'), ('OFFMKT', 'Off Market'), ('CANC', 'Cancelled')
                         ]

PRIORITY_TYPES = [
    ('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low'),
     ('URGENT', 'Urgent')
]

###############3 vehicles ################

# Add 'realestateapp.models.RequestMiddleware' to your settings.py MIDDLEWARE
primary_meter_options = (
		('Kilometers', 'Kilometers'),
		('Miles', 'Miles'),
	)
vehicle_type_options = (
		('Truck', 'Truck'),
		('Car', 'Car'),
        ('Pickup','Pickup'),
        ('Bus', 'Bus'),
        ('Trailer', 'Trailer'),
        ('Van','Van'),
        ('Tow Truck','Tow Truck'),
        ('Motorcycle','Motorcycle'),
	)
equipment_status_options = (
		('Active', 'Active'),
		('Inactive', 'Inactive'),
	)
oil_options = (
		('Petrol', 'Petrol'),
		('Diesel', 'Diesel'),
        ('Electric', 'Electric')
	)
Carrier_Type= [
    ('Truck', 'Truck'),
	('Car', 'Car'),
    ('Pickup','Pickup'),
    ('Aeropplane','Aeropplane'),
    ('Ship','Ship'),
    ('Bus', 'Bus'),
    ('Trailer', 'Trailer'),
    ('Van','Van'),
    ('Bajaaj','Bajaaj'),
    ('Bike','Bike'),
    ('Other','Other'),
    
    ]
Weight_Units=[
        ("KGs","KGs"),
        ("Ton","Ton"),
        ("Other","Other"),
    ]
Shipment_Status=[
        ("Booked","Booked"),
        ("Loaded","Loaded"),
        ("Dispatched","Dispatched"),
        ("Enroute","Enroute"),
        ("Delivered","Delivered"),
        ("Unknown","Unknown"),
        ("Other","Other"),
    ]
Transport_Mode=[
        ("Road","Road"),
        ("Air","Air"),
         ("Sea","Sea"),
    ]
##############3 healthcare #########3
SAMPLE_TYPES=[('BLOOD', 'Blood'), ('URINE', 'Urine'), ('TISSUE', 'Tissue'),('SWAB', 'Swab'), ('OTHER', 'Other')]


    # Generic Status for the event lifecycle
GENERIC_STATUS_CHOICES = [
    ('ACTIVE', 'Active/Open'),
    ('COMPLETED', 'Completed'),
    ('CANCELLED', 'Cancelled'),
    ('PENDING', 'Pending'),
    ('ON_HOLD', 'On Hold'),
    # Add more generic statuses as needed based on your overall ERP workflow
    ]

