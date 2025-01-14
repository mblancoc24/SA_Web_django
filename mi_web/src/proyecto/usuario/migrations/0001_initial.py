# Generated by Django 4.1.7 on 2023-03-21 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tipo', models.CharField(max_length=200)),
                ('estado', models.BooleanField(default=False)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('usuarios', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='profesor',
            fields=[
                ('id_profesor', models.AutoField(primary_key=True, serialize=False)),
                ('Cedula', models.CharField(max_length=25)),
                ('nombre', models.CharField(max_length=18)),
                ('primer_apellido', models.CharField(max_length=18)),
                ('segundo_apellido', models.CharField(max_length=18)),
                ('correo_profesor', models.CharField(max_length=100)),
                ('puesto_educativo', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='usuario.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='estudiantes',
            fields=[
                ('id_estudiante', models.AutoField(primary_key=True, serialize=False)),
                ('Cedula', models.CharField(max_length=22)),
                ('nombre', models.CharField(max_length=18)),
                ('primer_apellido', models.CharField(max_length=18)),
                ('segundo_apellido', models.CharField(max_length=18)),
                ('fecha_nacimiento', models.DateField()),
                ('phone_tutor', models.IntegerField(default=0)),
                ('correo_estudiante', models.CharField(max_length=60)),
                ('password', models.CharField(max_length=30)),
                ('pago_realizado', models.BooleanField(default=False)),
                ('documentos_presentados', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='usuario.usuarios')),
            ],
        ),
    ]
