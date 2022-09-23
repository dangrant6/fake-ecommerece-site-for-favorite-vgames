from itertools import product
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
# Create your views here.


def calculate():
    y = 2
    return 1

def frontpage(request):
    x = calculate()
    products = Product.objects.all()[0:5]
    return render(request, 'front.html', {
        'products' : products
    })
