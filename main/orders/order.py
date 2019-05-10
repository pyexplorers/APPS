
'''
	A Module to perform all Order related activities.
	Such as Accept / Process / Cancel / Delete
'''
import datetime
import sys
import configs
sys.path.append(configs.MAIN_PATH)
from pytus.pyutils import read_json,write_json

# Define the ORDER Class to Process all the Orders
class Orders:

	def __init__(self,**kwargs):
		'''
			Initialize the given order
		'''
		self.items = kwargs.get('items')
		self.zip_code = kwargs.get('zip_code')
		self.order_datetime = datetime.datetime.now()
		self.order_verify = Order_Verify
		self.records_file = configs.JSON_FILE
		self.records = read_json(self.records_file)
		self.max_order_count = configs.MAX_ORDER_PER_ZIP
		self.price_final = configs.PRICES_ITEMS[self.items]

	def check_order(self):
		'''
			Check the Order for all entries such as items,zipcode
		'''
		return self.order_verify.check(items=self.items,zip_code=self.zip_code)

	def create_order(self):
		'''
			Add a new order to the Database
		'''
		self.records.append({'items':self.items,'zip_code':self.zip_code})
		return write_json(self.records_file,self.records)

	def check_pricing(self):
		'''
			For a given item and zip-code, define a price.
			Consider both normal and surge pricing.
		'''
		check_pricing = Pricing.check(zip_code=self.zip_code,records=self.records,max_order_count=self.max_order_count)
		if not bool(check_pricing):
			self.price_final = self.price_final + configs.PRICES_ITEMS_SURGE[self.items]
		return self.price_final

	def __call__(self):
		self.check_order()
		self.create_order()
		return Format_Order(self.check_pricing(),self.items)

class Format_Order:

	def __init__(self,pricing,items):
		self.pricing = pricing
		self.items = items
		self.message = 'Order Accepted and Placed Successfully . Priced at .. {}.. For items {} '.format(self.pricing,str(self.items))	

	def __str__(self):
		return self.message

class Pricing:
	'''
		A Class to determine normal or surge
	'''
	@staticmethod
	def check(**kwargs):
		'''
			Check and return pricing information
		'''
		zip_code,records,max_order_count = kwargs.get('zip_code'),kwargs.get('records'),kwargs.get('max_order_count')
		counter = 0
		for record in records:
			if record['zip_code'] == zip_code:
				counter += 1
				if counter >= max_order_count:
					return False
		return True

class Order_Verify:
	'''
		Check if the given order contains all attributes
	'''
	@staticmethod
	def check(**kwargs):
		'''
			Check for Valid Orders
		'''
		if not bool(kwargs.get('items')) or not bool(kwargs.get('zip_code')):
			raise Exception("Not Enough information to process the order. Please define Items with proper zipcode")

		if not len(str(kwargs.get('zip_code'))) == 6:
			raise Exception("Zip Code must contain 6 digits . Please enter a Valid zipcode")

		return True

if __name__ == "__main__":

	orders = Orders(items='idly',zip_code='600115')
	print(orders())