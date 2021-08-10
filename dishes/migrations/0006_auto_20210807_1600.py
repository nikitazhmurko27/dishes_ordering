# Generated by Django 3.2.5 on 2021-08-07 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0005_auto_20210726_2016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='dish',
            name='description',
        ),
        migrations.RemoveField(
            model_name='order',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='orderingredients',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_ingredients', to='dishes.order'),
        ),
    ]