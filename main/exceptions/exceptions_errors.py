'''
	Define User defined custom exceptions
'''
class Order_Items_Missing(Exception):

	def __init__(self):
		Exception.__init__()

	def __str__(self):
		return "Not Enough information to process the order. Please define Items with proper zipcode"

