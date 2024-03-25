from django.core.management import BaseCommand
from django.db import connection
from catalog.models import Category, Product
import json


class Command(BaseCommand):
    """Класс для работы с БД приложения catalog"""

    @staticmethod
    def json_read_categories():
        """Staticmethod считывает данные из json файла с категориями."""
        with open('fixtures/category.json', 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_read_products():
        """Staticmethod считывает данные из json файла с продуктами."""
        with open('fixtures/product.json', 'r') as file:
            data = json.load(file)
        return data

    # Здесь мы получаем данные из фикстурв с продуктами

    def handle(self, *args, **options):
        """Функция очищает БД и записывает новые данные из фикстуры."""
        Product.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("""ALTER SEQUENCE catalog_product_id_seq RESTART WITH 1""")
        self.stdout.write(self.style.SUCCESS('Данные о продуктах успешно удалены'))
        Category.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("""ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1""")
        self.stdout.write(self.style.SUCCESS('Данные о категориях успешно удалены'))

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(name=category['fields']['name'], description=category['fields']['description'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        self.stdout.write(self.style.SUCCESS('Категории товаров успешно созданы'))

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(
                Product(name=product['fields']['name'],
                        description=product['fields']['description'],
                        img=product['fields']['img'],
                        # получаем категорию из базы данных для корректной связки объектов
                        category=Category.objects.get(pk=product['fields']['category']),
                        price=product['fields']['price'],
                        created_at=product['fields']['created_at'],
                        updated_at=product['fields']['updated_at']
                        )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS('Наименование товаров успешно созданы'))
