# Generated by Django 4.1.7 on 2023-03-29 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_alter_class_schedule_alter_class_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentID', models.CharField(max_length=30, unique=True)),
                ('dob', models.DateField(max_length=15)),
                ('lName', models.CharField(max_length=30)),
                ('fName', models.CharField(max_length=30)),
                ('last4Digits', models.CharField(max_length=15)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('email', models.CharField(blank=True, max_length=256, null=True)),
                ('accountInfo', models.CharField(blank=True, max_length=256, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('classes', models.ManyToManyField(related_name='classes', to='classes.class')),
            ],
        ),
    ]
