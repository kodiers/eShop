from django.contrib.auth.forms import AuthenticationForm
from shop.models import *
from django import template
register = template.Library()

@register.inclusion_tag("login.html") # Not used in this version
def login_form():
    form = AuthenticationForm()
    return {'form' : form}

@register.inclusion_tag("menu.html", takes_context=True)
def menu(context):
    context['page_categories'] = PageCategory.objects.all()
    context['goods_categories'] = CategoryGoods.objects.all()
    return {'page_categories':context['page_categories'], 'goods_categories':context['goods_categories']}
