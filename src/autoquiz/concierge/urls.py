from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^getTargetDoc$', views.getTargetDoc, name='getTargetDoc'),
	url(r'^about$', views.about, name='about')
]
