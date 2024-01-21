from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def homepage(request):
    data = {
        'popular_products': Product.objects.order_by('goods_sold')[:4]
    }
    return render(request, 'homepage.html', data)


def catalog(request, category_id='all', sort=None):
    if category_id == 'all':
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(product_type=category_id)
    if sort:
        product_list = product_list.order_by(sort)
    paginator = Paginator(product_list, 12)  # Разбиваем на 10 элементов на страницу

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если параметр 'page' не является целым числом, отображаем первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если параметр 'page' превышает максимальное количество страниц, отображаем последнюю
        products = paginator.page(paginator.num_pages)

    data = {
        'product_list': products,
        'categories': Product_type.objects.all(),
        'category_id': category_id,
    }

    return render(request, 'catalog.html', data)


def detailed_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    data = {
        'product': product,
    }
    return render(request, 'detailed_product.html', data)


def about(request):
    return render(request, 'about-us.html')
