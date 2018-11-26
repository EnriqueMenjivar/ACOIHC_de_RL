
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalancePeriodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo_deudor', models.FloatField(default=0.0)),
                ('saldo_acreedor', models.FloatField(default=0.0)),
                ('saldo_deudor_h', models.FloatField(default=0.0)),
                ('saldo_acreedor_h', models.FloatField(default=0.0)),
                ('cuenta_balance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogo.Cuenta')),
                ('hija_balance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogo.CuentaHija')),
            ],
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio_periodo', models.DateField()),
                ('final_periodo', models.DateField()),
                ('estado_periodo', models.BooleanField(default=False)),
                ('periodo_ajuste', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='balanceperiodo',
            name='periodo_balance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='periodo.Periodo'),
        ),
    ]
