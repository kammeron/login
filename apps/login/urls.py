from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register', views.register),
	url(r'^login', views.login),
	url(r'^logout', views.logout),
	url(r'^quotes', views.quotes),
	url(r'^add_quote', views.add_quote),
	url(r'^delete_quote/(?P<quote_id>\d+)/$', views.delete_quote),
	url(r'^myaccount/(?P<user_id>\d+)/$', views.edit_user),
	url(r'^user/(?P<user_id>\d+)/$', views.user_page),
	url(r'^edit_process', views.edit_process),
	url(r'^like_process/(?P<quote_id>\d+)/$', views.like_process),
]