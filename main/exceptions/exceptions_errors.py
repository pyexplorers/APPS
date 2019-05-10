'''
	Define User defined custom exceptions
'''
class Invalid_Code(Exception):

	def __init__(self):
		Exception.__init__(self)

	def __str__(self):
		return "Invalid zipcode. Please define Items with proper zipcode"

class Order_Items_Missing(Exception):

	def __init__(self):
		Exception.__init__(self)

	def __str__(self):
		return "Not Enough information to process the order. Please define Items with proper zipcode"


