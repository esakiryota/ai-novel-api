# Generated by Django 4.1.7 on 2023-02-17 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apisite', '0004_novel_favorite_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='apisite.user'),
        ),
    ]