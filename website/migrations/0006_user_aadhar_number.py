# Generated by Django 4.1 on 2023-03-08 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_remove_csv_download_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='aadhar_number',
            field=models.CharField(default='111111111111', max_length=12),
            preserve_default=False,
        ),
    ]
