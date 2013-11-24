#__author__ = 'kodiers'
#from django.conf.urls import *
#from django.views.generic.detail import DetailView
#from django.views.generic.list import ListView
#from cms.models import Story, Category
#
#info_dict = {'queryset':Story.objects.all(), 'template_object_name':'story'}
#
#urlpatterns = patterns('django.views.generic.detail',
#                       url(r'^(?P<slug>[-\w]+)$', DetailView.as_view(model=Story,), info_dict, name='cms_story'),
#                       url(r'^$', ListView.as_view(model=Story,), info_dict, name='cms_home'),
#                       )
#
#urlpatterns += patterns('cms.views',
#    url(r'^category/(?P<slug>[-\w]+)/$', 'category', name='cms_category'),
#    url(r'^search/$', 'search', name='cms_search'),
#    )
