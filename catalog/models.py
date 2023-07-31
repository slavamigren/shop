from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование категории')
    description = models.TextField(**NULLABLE, verbose_name='Описание категории')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование продукта')
    description = models.TextField(**NULLABLE, verbose_name='Описание продукта')
    photo = models.ImageField(upload_to='catalog/', **NULLABLE, verbose_name='Фото')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Наименование категории')
    price = models.IntegerField(verbose_name='Цена')
    create_date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    change_date = models.DateField(verbose_name='Дата последнего изменения', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Contact(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя клиента')
    phone_number = models.CharField(max_length=15, verbose_name='Телефон клиента')
    user_text = models.TextField(verbose_name='Описание продукта')

    def __str__(self):
        return f'{self.name}, {self.phone_number}: {self.user_text}'

    class Meta:
        verbose_name = 'Контактные данные'
        verbose_name_plural = 'Контактные данные'