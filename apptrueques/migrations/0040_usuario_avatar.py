# Generated by Django 5.0.6 on 2024-06-26 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptrueques', '0039_publicacion_fecha_fin_promocion_usuario_bloqueado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
