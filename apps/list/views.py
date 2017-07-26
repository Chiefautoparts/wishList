from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Item


def index(request):
	checkID(request)
	user = User.objects.get(id=request.session.get('id'))
	items = Item.objects.all()
	context={
		'items': items,
		'user': user,

	}
	return render(request, 'list/index.html', context)

def makeItem(request):
	checkID(request)
	return render(request, 'list/createItem.html')

def createItem(request):
	checkID(request)
	status = Item.objects.makeItem(request.POST)
	if not status['valid']:
		for error in status['errors']:
			messages.error(request, error)
			return redirect('list:makeItem')
	else:
		messages.success(request, 'Item has been created')

	return redirect(reverse('list:lindex'))

def addToList(request, item_id, user_id):
	checkID(request)
	status = Item.objects.add_to_list(item_id, user_id)
	if not status['valid']:
		for error in status['errors']:
			messages.error(request, error)
	else:
		messages.success(request, 'Item added to Your Wish List')
	return redirect('list:lindex')

def checkID(request):
	 if not request.session.get('id'):
	 	messages.error(request, 'Access Denied. Log in first.')
	 	return redirect('login:index')
# Create your views here.

    