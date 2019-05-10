'''
    Config Module for all Web-APIs interactions
'''
# Json dict keys - for storing employee data
API_USERS_ATTRIBUTES = ['emp_id','name_prefix','first_name','middle_initial','last_name','gender','email',
'father_name','mother_name','mother_maiden_name','dob','tob','age','weight','doj','quarter_joining','half_joining',
'year_joining','month_joining','month_name_joining','short_month','day_of_joining','dow_joining','short_dow',
'age_in_company','salary','last_hike','ssn','phone','place','county','city','state','zip','region','user_name','password']

# Full Path of the Datastore Json file
'''
    ** NOTE ** This file will be written and updated peridoically by a CRON/Daemon Process, fetching
    the data from required collections in Mongo DB.
'''
DATASTORE_JSON_FILE_CACHES = 'D:\\ArunChandramouli\\code\\pythonics\\users_records\\datastore\\sets\\json\\records.json'

'''
    *** For this task purpose I am hardcoding user info in a file ! But this has to be loaded via a secured approach ***
'''
# Set username and password for authentication process
AUTHORIZATION_INFORMATION = {'username':'admin','password':'admin'}
# Error to be raised when an invalid credential is sent
INVALID_CREDENTIALS_ERROR = {'ERROR_INVALID_CREDENTIALS':"Authorization was not successful"}

'''
    Define MongoDB Metadata
'''
# Define server name and port for connections
MONGO_SERVER_NAME = 'alpha-core-lnx'
MONGO_SERVER_PORT = 7000
# Define database name and collection name for insert/update/delete operations
MONGO_SERVER_DATABASE_NAME = 'users_management'
MONGO_SERVER_DATABASE_COLLECTION_NAME = 'users_metadata'