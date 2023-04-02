# Generated by Django 4.1.7 on 2023-03-30 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
        ('classes', '0003_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='program',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='classes', to='programs.program'),
            preserve_default=False,
        ),
    ]
