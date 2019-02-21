from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(_('Категория'), max_length=40)
    slug = models.SlugField(_('Slug'))

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list', kwargs={'category': self.slug})


class Brand(models.Model):
    name = models.CharField(_('Производитель'), max_length=40)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_('Название'), max_length=50)
    description = models.TextField(_('Описание'))
    category = models.ForeignKey(verbose_name=_('Категория'), to=Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(verbose_name=_('Производитель'), to=Brand, on_delete=models.PROTECT)
    price = models.DecimalField(_('Цена'), max_digits=10, decimal_places=2)
    quantity = models.IntegerField(_('Количество'), default=20)
    available = models.BooleanField(_('Доступен'), default=True)
    image = models.ImageField(_('Изображение'), upload_to='products')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'category': self.category.slug, 'pk': self.pk})