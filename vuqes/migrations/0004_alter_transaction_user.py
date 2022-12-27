# Generated by Django 4.1.3 on 2022-12-21 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vuqes', '0003_alter_bankaccount_balance_alter_bankaccount_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
