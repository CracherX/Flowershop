Фfrom django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


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


def search(request):
    query = request.GET.get('srch')
    if query:
        results = Product.search_by_name(query)
    else:
        results = Product.objects.none()
    return render(request, 'search.html', {'results': results})


@login_required
def add_to_favorite(request, product_id):
    user_favorite, created = Favorite.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)

    # Добавляем товар в избранное пользователя
    user_favorite.products.add(product)

    return redirect('favorite')


@login_required
def view_favorite(request):
    user_favorite = Favorite.objects.get(user=request.user)
    favorite_products = user_favorite.products.all()
    context = {
        'favorite_products': favorite_products,
    }
    return render(request, 'favorite.html', context)


@login_required
def remove_from_favorite(request, product_id):
    user_favorite = Favorite.objects.get(user=request.user)
    product = get_object_or_404(Product, pk=product_id)

    # Удаляем товар из избранного пользователя
    user_favorite.products.remove(product)

    return redirect('favorite')
