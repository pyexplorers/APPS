'''
    Do all Metaprogramming tasks
        1.) Validate REST API Credentials
        2.) Execute the authorize function and return results if credentials hold good else raise error
'''

'''
    A Decorator to validate the username and password of a REST API CALL
    and return results accordingly
'''
def authorize(**authorize_args):
    '''
        At high level obtain the authorization params
    '''
    def wrapped_function(function):
        '''
            Define a function to authorize user inputs
        '''
        def execute(*args,**kwargs):
            '''
                Verify, Execute and return the results
            '''
            credentials = args[1]
            return authorize_args['invalid_credentials_error'] if not (credentials == authorize_args['credentials']) \
                else function(*args,**kwargs)
        return execute
    return wrapped_function