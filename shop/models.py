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
    """Goods category admin"""
    prepopulated_fields = {'slug':('title',)}
    

class Goods(models.Model):
    """ Goods model"""
    title = models.CharField(max_length=100)
    good_price = models.FloatField()
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='img')
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
    list_display = ('title', 'good_price', 'quantity', 'active', 'modified')
    list_filter = ('title', 'good_price', 'quantity', 'active', 'modified')
    search_fields = ('title', 'info', 'good_price')


class OrderItem(models.Model):
    """Order item model"""
    goods = models.ForeignKey(Goods, related_name="+")
    unit_price = models.ForeignKey(Goods, related_name="+")
    quantity = models.IntegerField()
    total_price = models.IntegerField()

class Orders(models.Model):
    """Orders model"""
    ORDER_STATUS = (
        (0, 'Received'),
        (1, 'In Progress'),
        (2, 'Complete'),
    )
    owner = models.ForeignKey(User)
    items = models.ManyToManyField(OrderItem, related_name="+")
    total_cost = models.ForeignKey(OrderItem, related_name="+")
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


admin.site.register(CategoryGoods, CategoryGoodsAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Orders, OrdersAdmin)


