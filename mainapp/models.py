from django.shortcuts import reverse
from django.db import models


class Product(models.Model):
    name = models.CharField('Название товара', max_length=20, unique=True)
    price = models.DecimalField('Цена товара', max_digits=15, decimal_places=2)
    picture = models.ImageField('Картинка товара', upload_to='serveruploads', default='serveruploads/standard.jpg')
    description = models.TextField('Описание товара', default='Дополнительное описание отсутствует')
    product_type = models.ForeignKey('Product_type', on_delete=models.CASCADE, verbose_name='Категория товара')
    goods_sold = models.IntegerField('Продано всего', default=0)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_id': self.pk})

    class Meta:
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Product_type(models.Model):
    category_name = models.CharField('Название категории', max_length=20)

    class Meta:
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.category_name
