# Generated by Django 3.2.13 on 2022-06-12 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_image_available_extensions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ('-created_at',), 'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
    ]