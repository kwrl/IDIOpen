#encoding:utf-8

import unittest

class Test(unittest.TestCase):
	def __init__(self):
		super(Test, self).__init__();

	def setUp(self):
		self.myvar = "some value"

	def tearDown(self):
		""" Close everything that should be closed
		"""
		pass;
	
	def testTrue(self):
		pass;


if __name__== '__main__':
	unittest.main();

# EOF
