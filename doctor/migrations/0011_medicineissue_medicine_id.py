# Generated by Django 2.2.4 on 2019-10-31 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0010_remove_medicineissue_medicine_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicineissue',
            name='medicine_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='doctor.StockMedicine'),
            preserve_default=False,
        ),
    ]
