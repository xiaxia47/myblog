# Generated by Django 2.0.2 on 2018-05-23 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_auto_20180520_2147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_time']},
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(default='游客', max_length=50, verbose_name='昵称'),
        ),
    ]
