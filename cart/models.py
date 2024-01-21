from django.db import models
from django.db.models import Sum, F
from authorize.models import CustomUser


# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField('mainapp.Product', through='CartItem')

    def total_price(self):
        # Агрегируем сумму цен с учетом количества товаров в корзине
        return self.cartitem_set.aggregate(total_price=Sum(F('product__price') * F('quantity')))['total_price'] or 0

    def __str__(self):
        return f"Корзина для {self.user.username}"

    class Meta:
        verbose_name_plural = 'Корзины пользователей'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('mainapp.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name_plural = 'Товары в корзинах пользователей'
