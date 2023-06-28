# Generated by Django 4.2.1 on 2023-06-26 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setor', models.CharField(max_length=50)),
                ('corredor', models.PositiveIntegerField()),
                ('prateleira', models.PositiveIntegerField()),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.produto')),
            ],
        ),
    ]
