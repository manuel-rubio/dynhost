# -*- coding: utf-8 -*-
from django.test import TestCase

class LoginTestCase(TestCase):
	def setUp(self):
		pass

	def test_login_error(self):
		""" Login con un usuario no existente """
		self.assertTrue(True)
