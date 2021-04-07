from random import sample

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket(user):
    basket = []
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    product_list = Product.objects.all()
    return sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    products = Product.objects.all()[:4]
    content = {'title': 'Главная', 'products': products, 'basket': get_basket(request.user)}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category=category_item)

        content = {
            'title': 'продукты',
            'links_menu': links_menu,
            'category': category_item,
            'products': products_list,
            'basket': get_basket(request.user)
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    content = {
        'title': 'продукт',
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': ProductCategory.objects.all(),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', content)


def contact(request):
    content = {
        'title': 'Контакты',
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', content)
