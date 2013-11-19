from django.conf.urls import patterns, include, url
from shop.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eShop.views.home', name='home'),
    # url(r'^eShop/', include('eShop.foo.urls')),
    url(r'^$', MainGoodsListView.as_view(), name='shop_home'),
    url(r'^search/', search, name='shop_search'),
    url(r'register/', register),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
