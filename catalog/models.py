from django.db import models
from django.contrib.auth import get_user_model
NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    """product model работает с продуктами"""
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    img = models.ImageField(upload_to='poducts/', verbose_name='Фотография', **NULLABLE)
    category = models.ForeignKey("Category", related_name='Products', verbose_name="Категория",
                                 on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateField(verbose_name='Дата создания')
    updated_at = models.DateField(verbose_name='Дата последнего изменения')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = (
            ("cancel_product_publication", "Can cancel product publication"),
            ("change_product_description", "Can change product description"),
            ("change_product_category", "Can change product category"),
        )



class Category(models.Model):
    """category model работает с категориями товаров"""
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class BlogWrite(models.Model):
    heading = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, verbose_name='slug', **NULLABLE)
    photo = models.ImageField(upload_to='blogs/', verbose_name='Фотография', **NULLABLE)
    content = models.TextField(verbose_name='содержимое')
    created_at = models.DateField(verbose_name='Дата создания')
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    num_version = models.FloatField(verbose_name='номер версии')
    name_version = models.CharField(max_length=100, verbose_name='имя версии')
    is_active_version = models.BooleanField(default=True)

    def __str__(self):
        return self.name_version

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'