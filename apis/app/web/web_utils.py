'''
    Perform all activities related to the REST API Queries
    Connect with Database and do insert,fetch,update and delete operations
'''
import web_configs
from core.utilities.pyutils import Py_Utils
from core.metas.metas import authorize
from core.databases.mongoapp.query import Mongo_Utils

class Tasks:

    @staticmethod
    def set_database():
        '''
            Raise a connection with MongoDB
            Select database and collection
            Return the collections object
            Do Insert, Fetch, Update and Delete
        '''
        # Connect to the database
        connect_database = Mongo_Utils.get_connection(server_name=web_configs.MONGO_SERVER_NAME, server_port=web_configs.MONGO_SERVER_PORT)
        # Fetch the databse 
        fetch_database = Mongo_Utils.set_mongo_database(connection_object=connect_database, database_name=web_configs.MONGO_SERVER_DATABASE_NAME)
        # Return the Collection object
        return fetch_database.users_metadata

    @staticmethod
    def set_process_read_frequent():
        '''
            Set an infinite process to read the json files periodically and update the records
            ##TODO## -> This Function object will be triggered periodically and contents be updated
                from MongoDB
        '''
        #Class Variables to fetch & store the records -> File will be read once during module import
        Tasks.DATASTORE_JSON_RECORDS = Py_Utils.read_json(web_configs.DATASTORE_JSON_FILE_CACHES)['records']
        # Get all Usernames and store in a mapper
        Tasks.DATASTORE_JSON_RECORDS_USER_NAME_ARRAY  = [str(json_records['user_name']).lower() for json_records in Tasks.DATASTORE_JSON_RECORDS]
        return Tasks.DATASTORE_JSON_RECORDS
    
    @staticmethod
    @authorize(credentials=web_configs.AUTHORIZATION_INFORMATION,invalid_credentials_error=web_configs.INVALID_CREDENTIALS_ERROR)
    def get_users_information(mapper,authorize_info):
        '''
            Given a key-value pair, check the database for given combination and retreive required values.
            *** The function will be executed only if the User issues the REST calls with proper credentials. ***
            ***
                For all GET Operations instead of querying the Database, we shall take the
                records from the cache and return the filtered output. This cache will be
                updated periodically.
            ***
            :param mapper: User requested keys & values
            :param authorize_info: Auth Info required for processing REST Calls
            @return:
                Success -> All matching records that fit user's requests
                Exception -> Empty Array
        '''
        try:
            # Filter keys that are actually part of the system
            keys_api_users_attributes = [each_user_key for each_user_key in mapper if str(each_user_key[0]).lstrip().rstrip() in web_configs.API_USERS_ATTRIBUTES]
            # Do a Search on the existing datastore to filter records that fit the user's requests
            return [each_record for each_record in Tasks.DATASTORE_JSON_RECORDS for each_user_key in keys_api_users_attributes \
                if str(each_record[each_user_key[0]]).lower().__contains__(str(each_user_key[1]).lower())]
        except Exception as error:
            return ['ERROR']

    @staticmethod
    @authorize(credentials=web_configs.AUTHORIZATION_INFORMATION,invalid_credentials_error=web_configs.INVALID_CREDENTIALS_ERROR)
    def post_users_information(mapper,authorize_info,mongo_collection=None):
        '''
            Given user management data from user, make an entry into database and return the confirmation.
            *** The function will be executed only if the User issues the REST calls with proper credentials. ***
            ***
                For all POST Operations ,check the keys and values sent by the User and make an entry into the database.
                Invalid keys will be filtered and only valid keys will be processed.
                All keys required as a mandate shall be supplied by the User else user management DB will not
                be updated with user's requests.
                Invoke the supplied database and collection and insert the records.
            ***
            :param mapper: User recommended keys & values -> Dictionary format
            :param authorize_info: Auth Info required for processing REST Calls
            :param mongo_collection: Collection on which the records are to be inserted
            @return:
                Success -> Invoke database and add an entry
                            Return True if records are inserted else False
                Exception -> return ERROR
        '''
        try:
            '''
                Check if the User has posted all the required keys.
                Insert into MongoDB only if all the requiredkeys are found.
            '''
            if bool(Py_Utils.validate_users_keys(mapper,web_configs.API_USERS_ATTRIBUTES,
                    Tasks.DATASTORE_JSON_RECORDS_USER_NAME_ARRAY,check_user_exists=True)):
                '''
                    Do insert the records into the database -> This function will insert a new record(document) to the collection.
                    Mongo_Utils.insert_records -> This function will handle both single and bulk inserts.   
                '''
                Mongo_Utils.insert_records(collection_object=mongo_collection, records=mapper)
                # Return True -> Able to insert records into the database
                return {"data":True}
            # Return False -> Unable to insert records into the database
            return {"data":False}
        except Exception as error:
            # Return error on exception
            return {"data":"ERROR"}

    @staticmethod
    @authorize(credentials=web_configs.AUTHORIZATION_INFORMATION,invalid_credentials_error=web_configs.INVALID_CREDENTIALS_ERROR)
    def update_users_information(mapper,authorize_info,mongo_collection=None):
        '''
            Given user management data from user, update all entry in the database and return the confirmation.
            *** The function will be executed only if the User issues the REST calls with proper credentials. ***
            ***
                For all PUT Operations ,check the keys and values sent by the User and make an update in the database.
                Invalid keys will be filtered and only valid keys will be processed.
                All keys required as a mandate shall be supplied by the User else user management DB will not
                be updated with user's requests.
                Invoke the supplied database and collection and insert the records.
            ***
            :param mapper: User recommended keys & values -> Dictionary format
            :param authorize_info: Auth Info required for processing REST Calls
            :param mongo_collection: Collection on which the records are to be inserted
            @return:
                Success -> Invoke database and update all the documents in the collection.
                            Return True if records are inserted else False
                Exception -> return ERROR
        '''
        try:
            '''
                Check if the User has posted all the required keys.
                Make an update in MongoDB only if all the required keys are found.
            '''
            if bool(Py_Utils.validate_users_keys(mapper,web_configs.API_USERS_ATTRIBUTES,Tasks.DATASTORE_JSON_RECORDS_USER_NAME_ARRAY)):
                '''
                    Do insert the records into the database -> This function will insert a new record(document) to the collection.
                    Mongo_Utils.insert_records -> This function will handle both single and bulk inserts.   
                '''
                Mongo_Utils.update_records(collection_object=mongo_collection, records=mapper)
                # Return True -> Able to insert records into the database
                return {"data":True}
            # Return False -> Unable to insert records into the database
            return {"data":False}
        except Exception as error:
            # Return error on exception
            return {"data":"ERROR"}

    @staticmethod
    @authorize(credentials=web_configs.AUTHORIZATION_INFORMATION,invalid_credentials_error=web_configs.INVALID_CREDENTIALS_ERROR)
    def delete_users_information(mapper,authorize_info,mongo_collection=None):
        '''
            Given user management data from user, delete all entry in the database and return the confirmation.
            *** The function will be executed only if the User issues the REST calls with proper credentials. ***
            ***
                For all DELETE Operations ,check the keys and values sent by the User and make a deletion in the database.
                Invalid keys will be filtered and only valid keys will be processed.
                All keys required as a mandate shall be supplied by the User else user management DB will not
                be updated with user's requests.
                Invoke the supplied database and collection and delete the documents.
            ***
            :param mapper: User recommended keys & values -> Dictionary format.
            :param authorize_info: Auth Info required for processing REST Calls.
            :param mongo_collection: Collection on which the documents are to be deleted.
            @return:
                Success -> Invoke database and delete all the documents in the collection.
                            Return True if records are deleted else False.
                Exception -> return ERROR
        '''
        try:
            '''
                Check if the User has posted all the required keys.
                Make an deletion in MongoDB only if all the required keys are found.
            '''
            if bool(Py_Utils.validate_users_keys(mapper,web_configs.API_USERS_ATTRIBUTES,Tasks.DATASTORE_JSON_RECORDS_USER_NAME_ARRAY)):
                '''
                    Do insert the records into the database -> This function will insert a new record(document) to the collection.
                    Mongo_Utils.insert_records -> This function will handle both single and bulk inserts.   
                '''
                Mongo_Utils.delete_records(collection_object=mongo_collection, records=mapper)
                # Return True -> Able to insert records into the database
                return {"data":True}
            # Return False -> Unable to insert records into the database
            return {"data":False}
        except Exception as error:
            # Return error on exception
            return {"data":"ERROR"}
