from django.db import models
from django.db.models import permalink
from django.contrib import admin
from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image
import os
import datetime
from django.contrib.auth.models import User
import funct
from django.core.urlresolvers import reverse

# Create your models here.
class CategoryGoods(models.Model):
    """Goods category"""
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural="categories"

    def __unicode__(self):
        return self.title

class CategoryGoodsAdmin(admin.ModelAdmin):
    """Goods category admin"""
    prepopulated_fields = {'slug':('title',)}


class Goods(models.Model):
    """ Goods model"""
    title = models.CharField(max_length=100)
    category = models.ForeignKey(CategoryGoods)
    partnumber = models.CharField(max_length=50)
    good_price = models.FloatField()
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='img/')
    info = models.TextField(max_length=400, blank=True)
    active = models.BooleanField(default=True)
    modified = models.DateTimeField(default=datetime.datetime.now())


    class Meta:
        ordering =['modified']
        verbose_name_plural="Goods"

    def get_absolute_url(self):
        return "%s" % self.pk


class GoodsAdmin(admin.ModelAdmin):
    """Goods admin model"""
    list_display = ('partnumber', 'title', 'good_price', 'quantity', 'active', 'modified')
    list_filter = ('title', 'good_price', 'quantity', 'active', 'modified')
    search_fields = ('partnumber', 'title', 'info', 'good_price')


class OrderItem(models.Model):
    """Order item model"""
    order_id = models.IntegerField()
    goods = models.CharField(max_length=100) # Goods title
    partnumber = models.CharField(max_length=50)
    unit_price = models.FloatField()
    quantity = models.IntegerField()
    total_price_per_goods = models.FloatField()

class Orders(models.Model):
    """Orders model"""
    ORDER_STATUS = (
        (0, 'Received'),
        (1, 'In Progress'),
        (2, 'Complete'),
    )
    order_id = models.CharField(max_length=256)
    owner = models.ForeignKey(User)
    items = models.ManyToManyField(OrderItem, related_name="+")
    total_cost = models.FloatField()
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_modified = models.DateTimeField(default=datetime.datetime.now())
    date_closed = models.DateTimeField(blank=True)
    status = models.CharField(choices=ORDER_STATUS, default=0, max_length=12)

    class Meta:
        verbose_name_plural="Orders"
        ordering = ['-date_created']


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'total_cost', 'date_created', 'date_modified', 'date_closed', 'status')
    list_filter = ('id', 'owner', 'total_cost', 'date_created', 'date_modified', 'date_closed', 'status')
    search_fields = ('owner', 'goods', 'quantity', 'cost')

class PriceList(models.Model):
    name = models.CharField(max_length=255)
    pricelist = models.FileField(upload_to='prices', validators=[funct.import_document_validator])
    import_date = models.DateTimeField(auto_now=True)

class PriceListAdmin(admin.ModelAdmin):
    list_display = ('name', 'pricelist', 'import_date')

class PageCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Pages categories'

    def __unicode__(self):
        return self.name

class PageCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class Pages(models.Model):
    STATUS = (
        (0, "Needs edit"),
        (1, "Published"),
        (2, "Archived"),
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    category = models.ForeignKey(PageCategory)
    content = models.TextField()
    owner = models.ForeignKey(User)
    status = models.IntegerField(choices=STATUS, default=1)
    created = models.DateTimeField(default=datetime.datetime.now())
    modified = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        verbose_name_plural = "Pages"

    #@permalink
    def get_absolute_url(self):
        #return reverse("pages", (), {'slug':self.slug})
        return self.slug
        #return "%s" % self.pk

class PagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'created', 'modified')
    search_fields = ('title', 'content')
    list_filter = ('owner', 'status', 'created', 'modified')
    prepopulated_fields = {'slug':('title',)}

class Basket(models.Model):
    '''Basket model'''
    ORDER_STATUS = (
        (0, 'Received'),
        (1, 'In Progress'),
        (2, 'Complete'),
    )
    user = models.ForeignKey(User, null=True, blank=True)
    basket_id = models.CharField(max_length=2048) # session key
    item = models.CharField(max_length=100) #Goods title
    partnumber = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()
    sum_total = models.FloatField()
    created = models.DateTimeField(default=datetime.datetime.now(), null=True)
    modified = models.DateTimeField(default=None, null=True)
    comments = models.CharField(max_length=300, null=True, default=None)
    status = models.CharField(choices=ORDER_STATUS, default=0, max_length=12)
    order_number = models.IntegerField(null=True)


admin.site.register(CategoryGoods, CategoryGoodsAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(PriceList, PriceListAdmin)
admin.site.register(PageCategory, PageCategoryAdmin)
admin.site.register(Pages, PagesAdmin)

