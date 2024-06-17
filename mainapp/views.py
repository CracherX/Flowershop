from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse



def homepage(request):
    data = {
        'popular_products': Product.objects.order_by('goods_sold')[:4]
    }
    return render(request, 'homepage.html', data)


def catalog(request, category_id='all', sort=None):
    if request.user.is_authenticated:
        user_favorite = Favorite.objects.filter(user=request.user).first()
        favorite_product_ids = user_favorite.products.values_list('id', flat=True) if user_favorite else []
    else:
        favorite_product_ids = []
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
        'favorite_product_ids': favorite_product_ids,
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


@login_required
def add_to_favorite(request, product_id):
    user_favorite, created = Favorite.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)

    # Добавляем товар в избранное пользователя
    user_favorite.products.add(product)
    return HttpResponse(status=204)



@login_required
def view_favorite(request):
    try:
        user_favorite = Favorite.objects.get(user=request.user)
        favorite_products = user_favorite.products.all()
    except Favorite.DoesNotExist:
        favorite_products = None
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


def search(request):
    query = request.GET.get('srch')
    if query:
        products = Product.search_by_name(query)
    else:
        products = Product.objects.none()

    data = {
        'product_list': products,
        'categories': None,
        'category_id': None,
    }
    return render(request, 'catalog.html', data)


@login_required
def add_comment(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        text = request.POST.get('comment_text')

        Comment.objects.create(product=product, author=request.user, text=text)

    return redirect('product_detail', product_id=product_id)


def confid(request):
    return render(request, 'politika.html')