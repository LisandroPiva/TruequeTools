# Generated by Django 5.0.6 on 2024-06-29 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptrueques', '0045_remove_usuario_notificaciones_notificacion_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
    ]
