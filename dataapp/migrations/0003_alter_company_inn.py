# Generated by Django 4.1.5 on 2023-03-19 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataapp', '0002_alter_deal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='inn',
            field=models.CharField(db_index=True, default='', max_length=15, verbose_name='ИНН компании'),
        ),
    ]
