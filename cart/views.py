from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from mainapp.models import Product


# Create your views here.

@login_required
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    context = {
        'cart': cart,
    }

    return render(request, 'cart_view.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    # Проверяем, что товар принадлежит корзине пользователя
    if cart_item.cart.user != request.user:
        return redirect('cart_view')

    # Удаляем товар из корзины
    cart_item.delete()

    return redirect('cart_view')


@login_required
def increase_quantity(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')


@login_required
def decrease_quantity(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # Если количество товара равно 1, удаляем товар из корзины
        cart_item.delete()

    return redirect('cart_view')
