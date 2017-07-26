from __future__ import unicode_literals

from django.db import models
from ..login.models import User

class ItemManager(models.Manager):
	def makeItem(self, postData):
		status={'valid':True, 'errors':[]}
		if not postData['name'] or len(postData['name']) < 3:
			status['valid']=False
			status['errors'].append('Invalid Item. Check your porduct')

		item = Item.objects.filter(name=postData['name'])

		if status['valid'] is False:
			try:
				status['errors'].append('Item was not created. Try agian')
			except:
				item = Item.objects.create(name=postData['name'], owner=User.objects.get(id=postData['owner']))
				item.save()
		return status

	def add_to_list(self, item_id, user_id):
		status={'valid':True, 'errors':[]}
		try:
			item = Item.objects.get(id=item_id)
			item.wanted.add(user_id)
		except IntegrityError as e:
			status['valid']=False
			status['errors'].append(e.message)

		return status

	
class Item(models.Model):
	name = models.CharField(max_length=255)
	owner = models.ForeignKey('login.User', related_name='owner')
	wanted = models.ManyToManyField('login.User', related_name='wanted')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	objects = ItemManager()

	def __str__(self):
		return self.name