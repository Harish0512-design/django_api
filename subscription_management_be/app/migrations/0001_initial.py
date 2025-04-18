# Generated by Django 5.1.7 on 2025-03-15 05:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=45, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('billing_cycle', models.CharField(choices=[('Monthly', 'Monthly'), ('Quarterly', 'Querterly'), ('Yearly', 'Yearly')], max_length=15)),
                ('trail_period_days', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=55)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Canceled', 'Canceled'), ('Expired', 'Expired'), ('Paused', 'Paused')], max_length=15)),
                ('is_auto_renew', models.BooleanField(default=True)),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.profile')),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.subscriptionplan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='USD', max_length=10)),
                ('payment_status', models.CharField(choices=[('Success', 'Success'), ('Failed', 'Failed'), ('Pending', 'Pending')], max_length=25)),
                ('payment_method', models.CharField(choices=[('CreditCard', 'CreditCard'), ('PayPal', 'PayPal'), ('Gpay', 'Gpay'), ('PhonePe', 'PhonePe'), ('DebitCard', 'DebitCard')], max_length=15)),
                ('transaction_id', models.CharField(max_length=455, unique=True)),
                ('payment_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.profile')),
                ('subscription_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.subscription')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=100, unique=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'), ('Overdue', 'Overdue')], max_length=15)),
                ('due_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.profile')),
                ('subscription_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.subscription')),
            ],
        ),
    ]
