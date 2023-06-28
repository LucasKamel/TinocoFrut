# Generated by Django 4.2.1 on 2023-06-27 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_cadastro_alter_venda_preco_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecursosHumanos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('carga_horaria', models.IntegerField()),
                ('folha_de_ponto', models.FileField(upload_to='folhas_ponto/')),
                ('setor', models.CharField(max_length=50)),
                ('funcionario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.cadastro')),
            ],
        ),
    ]