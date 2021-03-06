import unittest
import json

from app import create_app
from app.api.v1.model.sales import Sales

class TestInvalidData(unittest.TestCase):
	"""
	class to test sales endpoint invalid data
	"""
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'
		payload = {'role': 'admin', 'password': '1234', 'email': 'admin@gmail.com'}
		response = self.test.post('/api/v1/users/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		token = data['result']
		self.headers = {'X-API-KEY':'{}'.format(token)}

	def tearDown(self):
		self.test = None
		self.content_type = None


	# test if user enter an invalid json  payload
	def test_invalid_payload(self):
		payload = {'productId':0,'quantity':10,'xyz':''}
		response = self.test.post('/api/v1/sales/',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'invalid payload'})

	# test if user enters an invalid data type
	def test_invalid_data_type(self):
		payload = {'productId':0,'quantity':'0'}
		response = self.test.post('/api/v1/sales/',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,400)
		self.assertEqual(data['message'],'Input payload validation failed')

	# test quantity less than 1
	def test_min_quantity(self):
		payload = {'productId':0,'quantity':-90}
		response = self.test.post('/api/v1/sales/',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'quantity can not be less than one'})

	# test id less than 1
	def test_min_id(self):
		payload = {'productId':-20,'quantity':90}
		response = self.test.post('/api/v1/sales/',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'productId can not be less than zero'})

	# test out range profuct id
	def test_max_id(self):
		payload = {'productId':20,'quantity':90}
		response = self.test.post('/api/v1/sales/',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'invalid product id'})


class TestValidData(unittest.TestCase):
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'
		payload = {'role': 'admin', 'password': '1234', 'email': 'admin@gmail.com'}
		response = self.test.post('/api/v1/users/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		token = data['result']
		self.headers = {'X-API-KEY':'{}'.format(token)}
		self.product = {'name': 'omo', 'quantity': 21, 'category': 'furniture','moq':0,'price':100}
		self.test.post('/api/v1/products/',content_type=self.content_type,
			data=json.dumps(self.product),headers=self.headers)
		self.payload = {'quantity':10,'productId':0}

	def tearDown(self):
		self.test = None
		self.content_type = None
		self.product = None
		self.payload = None
		Sales.sales.clear()

	def test_add_sales(self):
		response = self.test.post('/api/v1/sales/',content_type=self.content_type,
			data=json.dumps(self.payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(data,{'result': 'sales added'})
		self.assertEqual(response.status_code,201)


	def test_get_all_sales(self):
		response = self.test.post('/api/v1/sales/',content_type=self.content_type,
			data=json.dumps(self.payload),headers=self.headers)
		self.assertEqual(response.status_code,201)
		response = self.test.get('/api/v1/sales/',content_type=self.content_type
			,headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,200)

	def get_one_sales(self):
		response = self.test.post('/api/v1/sales/',content_type=self.content_type,
			data=json.dumps(self.payload),headers=self.headers)
		self.assertEqual(response.status_code,201)
		response = self.test.get('/api/v1/sales/{}'.format(0),content_type=self.content_type)
		self.assertEqual(response.status_code,200)


if __name__ == '__main__':
	unittest.main()