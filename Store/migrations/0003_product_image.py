# Generated by Django 5.1.3 on 2024-11-25 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_product_alter_customer_email_alter_order_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
