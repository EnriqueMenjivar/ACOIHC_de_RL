
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('periodo', '0001_initial'),
        ('catalogo', '0001_initial'),
        ('contabilidad_general', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asignar_Cif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_cif', models.CharField(max_length=100)),
                ('porcentaje_cif', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Asignar_Mano_Obra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_horas_empleado', models.FloatField()),
                ('cantidad_empleados', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Asignar_Materia_Prima',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_mp', models.FloatField()),
                ('precio_unitario_mp', models.FloatField()),
                ('nombre_mp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogo.CuentaHija')),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cargo', models.CharField(max_length=100)),
                ('sueldo_base', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_empleado', models.CharField(max_length=100)),
                ('apellido_empleado', models.CharField(max_length=100)),
                ('dui_empleado', models.CharField(max_length=100)),
                ('Nisss_empleado', models.CharField(max_length=100)),
                ('Nafp_empleado', models.CharField(max_length=100)),
                ('años_empleado', models.FloatField()),
                ('cargo_empleado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad_costos.Cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Entrada_Salida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_es', models.DateField()),
                ('cantidad_unidades', models.IntegerField()),
                ('precio_unitario', models.FloatField()),
                ('tipo_movimiento', models.BooleanField(default=False)),
                ('cabeza_kardex', models.BooleanField(default=False)),
                ('cola_kardex', models.BooleanField(default=False)),
                ('siguiente_kardex', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kardex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_existencia', models.IntegerField()),
                ('precio_unitario_peps', models.FloatField()),
                ('cuenta_kardex', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogo.CuentaHija')),
            ],
        ),
        migrations.CreateModel(
            name='Planilla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isss_planilla', models.FloatField()),
                ('afp_planilla', models.FloatField()),
                ('vacacion_planilla', models.FloatField()),
                ('aguinaldo_planilla', models.FloatField()),
                ('insaforp', models.FloatField()),
                ('salario_total', models.FloatField()),
                ('empleado_planilla', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad_costos.Empleado')),
                ('periodo_planilla', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='periodo.Periodo')),
            ],
        ),
        migrations.CreateModel(
            name='Proceso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proceso_siguiente', models.CharField(max_length=100)),
                ('nombre_proceso', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Programacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_programacion', models.DateField()),
                ('producto_programacion', models.CharField(max_length=100)),
                ('cantidad_programacion', models.IntegerField()),
                ('estado_programacion', models.BooleanField(default=False)),
                ('periodo_programacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='periodo.Periodo')),
            ],
        ),
        migrations.AddField(
            model_name='proceso',
            name='programacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad_costos.Programacion'),
        ),
        migrations.AddField(
            model_name='entrada_salida_respaldo',
            name='kardexr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad_costos.Kardex'),
        ),
        migrations.AddField(
            model_name='entrada_salida_respaldo',
            name='periodo_esr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='periodo.Periodo'),
        ),
        migrations.AddField(
            model_name='entrada_salida',
            name='kardex',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad_costos.Kardex'),
        ),
        migrations.AddField(
            model_name='entrada_salida',
            name='periodo_es',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='periodo.Periodo'),
        ),
        migrations.AddField(
            model_name='asignar_materia_prima',
            name='proceso_mp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad_costos.Proceso'),
        ),
        migrations.AddField(
            model_name='asignar_mano_obra',
            name='cargo_mo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad_costos.Cargo'),
        ),
        migrations.AddField(
            model_name='asignar_mano_obra',
            name='proceso_mo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad_costos.Proceso'),
        ),
        migrations.AddField(
            model_name='asignar_cif',
            name='proceso_cif',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad_costos.Proceso'),
        ),
    ]
