# Generated by Django 2.2.6 on 2020-02-20 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0020_auto_20200210_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='isDependent',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='relative', max_length=100)),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.Prescription')),
            ],
        ),
    ]
