# Generated by Django 2.2.5 on 2020-02-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0014_auto_20200203_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='prescription_no_of_doctor',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name='prescription',
            unique_together={('doctor_id', 'prescription_no_of_doctor')},
        ),
    ]