# Generated by Django 2.0 on 2019-04-29 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='chaqueta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_serie', models.IntegerField()),
                ('talla', models.CharField(max_length=30)),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('correo', models.EmailField(max_length=256)),
                ('direccion', models.CharField(max_length=256)),
                ('ciudad', models.CharField(max_length=256)),
                ('numero', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Infopedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField()),
                ('medio_pago', models.CharField(max_length=512)),
                ('envio_domicilio', models.CharField(max_length=512)),
                ('retiro_tienda', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Modelochaqueta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temporada', models.CharField(max_length=30)),
                ('tendencia', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integrantes.Cliente')),
            ],
        ),
        migrations.AddField(
            model_name='infopedido',
            name='pedido',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='integrantes.Pedido'),
        ),
        migrations.AddField(
            model_name='chaqueta',
            name='info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integrantes.Infopedido'),
        ),
        migrations.AddField(
            model_name='chaqueta',
            name='modelo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integrantes.Modelochaqueta'),
        ),
    ]