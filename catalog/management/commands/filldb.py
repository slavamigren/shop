from django.core.management import BaseCommand
from catalog.models import Category, Product
import os, json


class Command(BaseCommand):

    def add_arguments(self, parser):
        """Принимает название json файла c фикстурами"""
        parser.add_argument('filename', type=str, help=u'Name of json file with fixtures')

    def handle(self, *args, **kwargs):
        """
        В командной строке после команды нужно написать название json файла
        с фикстурами для заполнения бд
        """
        filename = kwargs.get('filename', 'data.json')
        if not os.path.exists(filename):
            print('File does not exist')
            return None

        # разбираем файл с фикстурами
        with open(filename, 'r', encoding='utf-8') as file:
            categories = []
            products = []
            for elem in json.load(file):
                if elem['model'] == 'catalog.category':
                    categories.append(Category(pk=elem['pk'], **elem['fields']))
                else:
                    temp_dict = elem['fields']
                    temp_dict['category_id'] = temp_dict['category']
                    del temp_dict['category']
                    products.append(Product(**temp_dict))
        # очищаем бд
        all_categories = Category.objects.all()
        all_categories.delete()

        # записываем данные из фикстур
        Category.objects.bulk_create(categories)
        Product.objects.bulk_create(products)


