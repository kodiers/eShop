# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, RequestContext, render
from django.db.models import Q
from models import Goods, CategoryGoods, Pages, PageCategory, Orders, OrderItem
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template import loader
from django.core.context_processors import csrf
from django.contrib.auth import login, logout, authenticate
from django.views.generic.list import ListView
from shop.forms import *

# Functions

def register(request):
    """ Register view function. Show registration form"""
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/reg_success/")
    else:
        form = MyUserCreationForm()
    templ = loader.get_template("register.html")
    cont = RequestContext(request, {"form":form})
    cont.update(csrf(request))
    return HttpResponse(templ.render(cont))

def search(request):
    """Return list of goods, that contains searched string in title or in info fields."""
    if 'q' in request.GET:
        term = request.GET['q']
        story_list = Goods.objects.filter(Q(title__contains=term )|Q(info__contains=term))
        heading = "Search results"
    return render_to_response("main.html", locals())

def login_form(request):
    """Handle logins"""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            usr = authenticate(username=username, password=password)
            if usr is not None:
                if usr.is_active:
                    login(request, usr)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponseRedirect("/register/")
    else:
        form = AuthenticationForm()
        t = loader.get_template("login.html")
        c = RequestContext(request, {'form': form})
        c.update((csrf(request)))
        return HttpResponse(t.render(c))

def page_category(request, slug):
    """Return list of pages in category"""
    category = get_object_or_404(PageCategory, slug=slug)
    pages = Pages.objects.filter(category=category)
    heading = category.name
    return render_to_response("list_pages.html", locals())

def goods_category(request, slug):
    """Return list of goods in category"""
    category = get_object_or_404(CategoryGoods, slug=slug)
    goods = Goods.objects.filter(category=category)
    heading = category.title
    return render_to_response("list_goods.html", locals())


# Classes

class MainGoodsListView(ListView):
    """Main page view. Show list of goods"""
    template_name = "main.html"
    queryset = Goods.objects.filter(active=True)
    context_object_name = "goods_list"