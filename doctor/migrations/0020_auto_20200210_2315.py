# Generated by Django 2.2.6 on 2020-02-10 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0019_medicineissue_issue_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicineissue',
            name='issue_status',
            field=models.BooleanField(default=0),
        ),
    ]
