from __future__ import unicode_literals
from django.db import models, IntegrityError
import bcrypt
import re

class UserManager(models.Manager):
	def registerVal(self, postData):
		results = {'status':True, 'errors':[], 'user':None}
		if not postData['name'] or len(postData['name']) < 3:
			results['status']=False
			results['errors'].append('enter a valid name')
		if not postData['username'] or len(postData['username']) < 3:
			results['status']=False
			results['errors'].append('enter a valid username')
		if not postData['password'] or len(postData['password']) < 8:
			results['status']=False
			results['errors'].append('please enter a valid password')
		if postData['password'] != postData['passvalid']:
			results['status'] = False
			results['errors'].append('Passwords do not match')

		user = User.objects.filter(username=postData['username'])

		if results['status']:
			try:
				user = User.objects.create(name=postData['name'], username=postData['username'], password=(bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())))
				user.save()
				results['user']=user
			except IntegrityError as e:
				results['status']=False
				if 'UNIQUE constraint'in e.message:
					results['errors'].append('username already in system')
				else:
					results['errors'].append(e.message)
		return results

	def loginVal(self, postData):
		results = {'status':True, 'errors':[], 'user':None}
		try:
			user = User.objects.get(username=postData['username'])
			if user.password == bcrypt.hashpw(postData['password'].encode(), user.password.encode()):
				pass
			else:
				raise Exception()
		except Exception as e:
			results['status']=False
			results['errors'].append('incorrect Username or password')

		if results['status']:
			results['user'] = user
		return results

class User(models.Model):
	name = models.CharField(max_length=255)
	username= models.CharField(max_length=255)
	password = models.CharField(max_length=255)

	objects = UserManager()