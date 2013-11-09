from django.db import models
from django.contrib import admin
from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image
import os
import datetime
from django.contrib.auth.models import User

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
    prepopulated_fields = {'slug':('title',)}

class Price(models.Model):
    cost = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    good_title = models.ForeignKey(Goods)
    modified = models.DateTimeField(default=datetime.datetime.now())

class Goods(models.Model):
    title = models.CharField(max_length=100)
    good_price = models.ForeignKey(Price)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='img')
    info = models.TextField(max_length=400, blank=True)
    active = models.BooleanField(default=True)
    modified = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        ordering =['modified']

    def get_absolute_url(self):
        return "%s" % self.pk

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('title', 'good_price', 'quantity', 'active', 'modified')
    list_filter = ('title', 'good_price', 'quantity', 'active', 'modified')
    search_fields = ('title', 'info', 'good_price')

class Orders(models.Model):
    # TODO: create multiple goods in order for user
    # TODO: change Orders model and create OrdersAdmin model
    ORDER_STATUS = (
        (0, 'Received'),
        (1, 'In Progress'),
        (2, 'Complete'),
    )
    owner = models.ForeignKey(User)
    #goods = models.ForeignKey(Goods)
    quantity = models.IntegerField(default=0)
    #cost = quantity * goods.good_price
    date = models.DateTimeField(default=datetime.datetime.now())

admin.site.register(CategoryGoods, GoodsCategoryAdmin)
admin.site.register(Goods, GoodsAdmin)


