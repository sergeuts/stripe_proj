# Generated by Django 4.1.3 on 2022-11-24 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'ordering': ['name'], 'verbose_name': 'Currency', 'verbose_name_plural': 'Currencies'},
        ),
        migrations.AlterModelOptions(
            name='orderitemslist',
            options={'ordering': ['order_no'], 'verbose_name': 'Order items list', 'verbose_name_plural': 'Order items list'},
        ),
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name': 'Tax', 'verbose_name_plural': 'Taxes'},
        ),
        migrations.AlterField(
            model_name='currency',
            name='rate',
            field=models.DecimalField(decimal_places=4, max_digits=10, verbose_name='Exchange rate to the USD'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount',
            field=models.PositiveSmallIntegerField(verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stripe_app.tax', verbose_name='Tax'),
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.PositiveIntegerField(verbose_name='Number'),
        ),
        migrations.AlterField(
            model_name='order',
            name='sum',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Order sum'),
        ),
        migrations.AlterField(
            model_name='orderitemslist',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='orderitemslist',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name='Item quantity'),
        ),
        migrations.AlterField(
            model_name='orderitemslist',
            name='sum',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Items price'),
        ),
        migrations.AlterField(
            model_name='orderitemslist',
            name='tax',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Tax'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='tax',
            field=models.PositiveSmallIntegerField(verbose_name='Tax'),
        ),
    ]
