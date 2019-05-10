'''
	A Module to perform all Utilities related operation
'''
import json
import logging
# Set Loggers
logging.basicConfig(level=logging.INFO)
pylog = logging.getLogger('Foodie')

# Define a function to read json file
def read_json(file_json):
	'''
		Read a json file and return the contents
		:param file_json: Json file full path
		@return:json contents
		@exception: Empty Content ~ {}
	'''
	try:
		with open(file_json,'r') as reader:
			return json.load(reader)
	except Exception as error:
		pylog.error(error)
		return {}

# Define a function to write to json file
def write_json(file_json,contents):
	'''
		Read a json file and return the contents
		:param file_json: Json file full path
		:param contents: Contents to be written to json file
	'''
	try:
		with open(file_json,'w') as json_writer:
			return json.dump(contents,json_writer)
	except Exception as error:
		pylog.error(error)
		return {}