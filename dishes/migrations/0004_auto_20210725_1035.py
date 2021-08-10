# Generated by Django 3.2.5 on 2021-07-25 10:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0003_alter_dishingredients_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dishingredients',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dish_ingredients', to='dishes.dish'),
        ),
    ]