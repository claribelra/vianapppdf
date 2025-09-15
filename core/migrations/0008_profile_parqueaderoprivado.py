from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_parqueaderoprivado_tarifa_dia_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='parqueaderoprivado',
            field=models.OneToOneField(
                to='core.parqueaderoprivado',
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
                blank=True,
                related_name='dueno_profile',
            ),
        ),
    ]
