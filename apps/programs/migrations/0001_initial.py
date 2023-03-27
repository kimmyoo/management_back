# Generated by Django 4.1.7 on 2023-03-21 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programName', models.CharField(max_length=250, unique=True)),
                ('programCode', models.CharField(max_length=250, unique=True)),
                ('length', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('isActive', models.BooleanField(default=True)),
                ('expiresAt', models.DateField(blank=True, max_length=15, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
