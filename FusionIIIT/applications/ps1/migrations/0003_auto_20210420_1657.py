# Generated by Django 3.1.5 on 2021-04-20 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('globals', '0003_auto_20191024_1242'),
        ('ps1', '0002_auto_20210406_2330'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stock',
            new_name='StockEntry',
        ),
        migrations.AlterModelTable(
            name='stockentry',
            table='StockEntry',
        ),
    ]