# Generated by Django 3.1.2 on 2020-10-28 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20201028_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='regional_restrictions',
            field=models.CharField(choices=[('anywhere', 'Anywhere (100% Remote Only)'), ('usa_only', 'USA Only'), ('north_america_only', 'North America Only'), ('europe_only', 'Europe Only'), ('americas_only', 'Americas Only'), ('canada_only', 'Canada Only'), ('emea_only', 'EMEA Only'), ('asia_only', 'Asia Only'), ('africa_only', 'Africa Only'), ('other', 'Other')], default='anywhere', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='company_uploads/'),
        ),
    ]
