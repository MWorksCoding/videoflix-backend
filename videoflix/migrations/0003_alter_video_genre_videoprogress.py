# Generated by Django 5.1.1 on 2024-10-23 08:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix', '0002_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='genre',
            field=models.CharField(choices=[('fitness', 'Fitness'), ('pets', 'Pets'), ('holiday', 'Holiday')], default='fitness', max_length=20),
        ),
        migrations.CreateModel(
            name='VideoProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.FloatField(default=0.0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videoflix.video')),
            ],
            options={
                'unique_together': {('user', 'video')},
            },
        ),
    ]
