from django.conf.urls import url
from . import views

app_name='list'
urlpatterns=[
	url(r'^lindex$', views.index, name='lindex'),
	url(r'^makeItem$', views.makeItem, name='makeItem'),
	url(r'^createItem$', views.createItem, name='createItem'),
]

