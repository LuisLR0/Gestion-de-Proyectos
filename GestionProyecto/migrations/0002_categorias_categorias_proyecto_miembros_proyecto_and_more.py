# Generated by Django 5.1.6 on 2025-03-14 20:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionProyecto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='categorias',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='categorias_proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionProyecto.categorias')),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionProyecto.proyectos')),
            ],
        ),
        migrations.CreateModel(
            name='miembros_proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False)),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionProyecto.proyectos')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='tareas',
            fields=[
                ('id_tarea', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('prioridad', models.CharField(choices=[('BAJA', 'Baja'), ('MEDIA', 'Media'), ('ALTA', 'Alta')], max_length=5)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_vencimiento', models.DateTimeField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionProyecto.categorias')),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionProyecto.proyectos')),
            ],
        ),
        migrations.CreateModel(
            name='tareas_proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionProyecto.proyectos')),
                ('id_tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionProyecto.tareas')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
