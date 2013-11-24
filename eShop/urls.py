from django.conf.urls import patterns, include, url
from shop.views import *
from django.views.generic.detail import DetailView
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

pages_dict = {'queryset':Pages.objects.all(), 'template_object_name':'page'}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eShop.views.home', name='home'),
    # url(r'^eShop/', include('eShop.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', MainGoodsListView.as_view(), name='shop_home'),
    url(r'^search/', search, name='shop_search'),
    url(r'register/', register),
    url(r'login/', login_form, name='login_form'),
    url(r'^page_category/(?P<slug>[-\w]+)/$', 'shop.views.page_category', name='page_category'),
    url(r'^goods_category/(?P<slug>[-\w]+)/$', 'shop.views.goods_category', name='goods_category'),
    url(r'^(?P<pk>[-\w]+)/$', DetailView.as_view(model=Goods)),
    url(r'^page_category/(?P<page_category>[-\w]+)/(?P<slug>[-\w]+)/$', pages_detail),
    url(r'^goods_category/(?P<goods_category>[-\w]+)/(?P<pk>[-\w]+)/$', DetailView.as_view(model=Goods)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

)
