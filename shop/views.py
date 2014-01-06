# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, RequestContext, render
from django.db.models import Q
from models import Goods, CategoryGoods, Pages, PageCategory, Orders, OrderItem, Basket
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template import loader
from django.core.context_processors import csrf
from django.contrib.auth import login, logout, authenticate
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from shop.forms import *
import random
import uuid
from django.core.urlresolvers import reverse

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
        goods_list = Goods.objects.filter(Q(title__contains=term )|Q(info__contains=term))
        heading = "Search results"
        #MainGoodsListView.as_view(queryset=Goods.objects.filter(Q(title__contains=term )|Q(info__contains=term)))
    return render_to_response("main.html", locals(), context_instance=RequestContext(request))

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
    return render_to_response("list_pages.html", locals(), context_instance=RequestContext(request))

def goods_category(request, slug):
    """Return list of goods in category"""
    category = get_object_or_404(CategoryGoods, slug=slug)
    goods = Goods.objects.filter(category=category)
    heading = category.title
    return render_to_response("list_goods.html", locals(), context_instance=RequestContext(request))

def pages_detail(request, page_category, slug):
    """Return detail of requested page"""
    pages = Pages.objects.get(slug=slug)
    templ = loader.get_template('shop/pages_detail.html')
    contex = RequestContext(request, {'pages':pages})
    return HttpResponse(templ.render(contex))

def add_basket(request):
    #Basket view( can change and delete items in basket)
    if request.method == 'POST':
        if 'del' in request.POST:
            basket_del = Basket.objects.get(pk=int(request.POST['b_pk']))
            basket_del.delete()
        elif 'save' in request.POST:
            basket_plus = Basket.objects.get(pk=int(request.POST['b_pk']))
            basket_plus.quantity = int(request.POST['quant'])
            basket_plus.sum_total = basket_plus.quantity * basket_plus.price
            basket_plus.save()
        else:
            good = Goods.objects.get(pk=int(request.POST['pk']))
            basket = Basket()
            if request.user.is_authenticated():
                basket.user = request.user
            if not request.session.exists(request.session.session_key):
                request.session.create()
            basket.basket_id = request.session.session_key
            basket.item = good.title
            basket.partnumber = good.partnumber
            basket.price = good.good_price
            basket.quantity = int(request.POST['quantity'])
            basket.order_number = random.randint(1, 1000000000)
            basket.sum_total = basket.quantity * basket.price
            basket.save()
        baskets = Basket.objects.filter(basket_id = request.session.session_key)
        summ = 0
        for bas in baskets:
            summ += bas.sum_total
        templ = loader.get_template("add_basket.html")
        context = RequestContext(request, {'baskets':baskets, 'summ':summ})
        return HttpResponse(templ.render(context))
    else:
        templ = loader.get_template("errors.html")
        error = "Get request! o.O"
        context = RequestContext(request, {'error':error})
        return HttpResponse(templ.render(context))

def add_order(request):
    #TODO: do a create order
    if request.method == 'POST':
        if 'payment_type' in request.POST:
            if request.POST['payment_type'] == 'card':
                summ = request.POST['total']
                template = loader.get_template("add_order.html")
                context = RequestContext(request, {'summary': summ})
                return HttpResponse(template.render(context))
        elif 'order' in request.POST:
            baskets = Basket.objects.filter(basket_id=request.session.session_key)
            orderitems = OrderItem()
            order = Orders()
            for basket in baskets:
                orderitems.order_sess = basket.basket_id
                orderitems.goods = basket.item
                orderitems.quantity = basket.quantity
                orderitems.total_price_per_goods = basket.sum_total
                orderitems.order_id = basket.order_number
                orderitems.partnumber = basket.partnumber
                orderitems.save()
            if request.user.is_authenticated():
                order.owner = request.user
            order.total_cost = float(request.POST['total'])
            order.address = request.POST['address']
            order.comments = request.POST['comments']
            order.billing_card = request.POST['billing_card']
            order.billing_number = request.POST['billing_number']
            order.billing_name = request.POST['billing_name']
            order.billing_date_mm = request.POST['billing_date_mm']
            order.billing_date_yy = request.POST['billing_date_yy']
            order.billing_cvv = request.POST['billing_cvv']
            order.save()
            template = loader.get_template("order_success.html")
            context = RequestContext(request, {'order_id': order.pk})
            return HttpResponse(template.render(context))


# Classes

class MainGoodsListView(ListView):
    """Main page view. Show list of goods"""
    template_name = "main.html"
    queryset = Goods.objects.filter(active=True)
    context_object_name = "goods_list"
    paginate_by = 15

class PagesDetailView(DetailView): #Not used in this version
    """Show pages content"""
    model = Pages
    slug_field = 'slug'
    template_name = 'shop/pages_detail.html'
    def get_context_data(self, **kwargs):
        context = super(PagesDetailView, self).get_context_data(**kwargs)
        return context


class GoodsDetailView(DetailView):
    model = Goods