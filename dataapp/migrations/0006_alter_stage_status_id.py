# Generated by Django 4.1.2 on 2023-01-27 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataapp', '0005_deal_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='STATUS_ID',
            field=models.CharField(db_index=True, max_length=35, verbose_name='Аббревиатура стадии сделки'),
        ),
    ]
