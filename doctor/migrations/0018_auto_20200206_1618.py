# Generated by Django 2.2.5 on 2020-02-06 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0017_auto_20200203_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthcentrestaff',
            name='user_id',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
