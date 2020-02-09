# Generated by Django 2.2.5 on 2020-02-03 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0009_remove_medicine_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicineissue',
            name='issue_status',
        ),
        migrations.RemoveField(
            model_name='medicineissue',
            name='non_issue_reason',
        ),
        migrations.AddField(
            model_name='medicineissue',
            name='dose',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='medicineissue',
            name='medicine_quantity',
            field=models.IntegerField(default=0),
        ),
    ]