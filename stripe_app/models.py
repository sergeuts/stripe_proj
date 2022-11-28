from django.db import models


class Item(models.Model):
    item_id = models.PositiveIntegerField(blank=False, default=0, verbose_name="Item id")
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(blank=False, max_digits=15, decimal_places=2, verbose_name="Price")
    currency = models.ForeignKey('Currency', blank=True, on_delete=models.PROTECT)
    tax = models.ForeignKey('Tax', blank=True, on_delete=models.PROTECT, verbose_name="Tax")

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.CharField(max_length=255, verbose_name="Description")
    rate = models.DecimalField(blank=False,  max_digits=10, decimal_places=4, verbose_name="Exchange rate to the USD")
    date = models.DateField(auto_now_add=True, verbose_name="Exchange rate on the date")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
        ordering = ['name']


class Order(models.Model):
    number = models.PositiveIntegerField(blank=False, verbose_name="Number")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    sum = models.DecimalField(blank=False, max_digits=15, decimal_places=2, verbose_name="Order sum")
    #items = models.ForeignKey('OrderItemsList', blank=True, on_delete=models.PROTECT, verbose_name="Item list")
    discount = models.ForeignKey('Discount', blank=True, on_delete=models.PROTECT)

    def __str__(self):
        #return f'№ {self.number} dated {self.date}'
        return str(self.number)


class OrderItemsList(models.Model):
    order_no = models.ForeignKey('Order', blank=True, on_delete=models.PROTECT, verbose_name="Order")
    item = models.ForeignKey('Item', blank=True, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(blank=False, verbose_name="Item quantity")
    sum = models.DecimalField(blank=False, max_digits=15, decimal_places=2, verbose_name="Items price")
    discount = models.DecimalField(blank=False, max_digits=15, decimal_places=2, verbose_name="Discount")
    tax = models.DecimalField(blank=True, max_digits=15, decimal_places=2, verbose_name="Tax")

    def __str__(self):
        return str(self.order_no)

    class Meta:
        verbose_name = 'Order items list'
        verbose_name_plural = 'Order items list'
        ordering = ['order_no']


class Discount(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    discount = models.PositiveSmallIntegerField(blank=False, verbose_name="Discount")

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=32, default='VAT', verbose_name="Name")
    tax = models.PositiveSmallIntegerField(blank=False, default=0, verbose_name="Tax")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Taxes'

'''
Item с полями(name, description, price)
    • Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
    • Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. 
    • Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
'''

def fill_table(table, values):
    if not table.objects.all().count():
        for n in values:
            r = table.objects.create(name=n)
            r.save()


def init_system_tables():
    fill_table(Gender, ['Male', 'Female'])

