# Generated by Django 5.2 on 2025-05-06 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serializerTopix', '0008_post_alter_comments_user_reaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField()),
                ('user_type', models.CharField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
