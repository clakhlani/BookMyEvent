# Generated by Django 4.0.3 on 2022-03-03 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventbooking', '0003_alter_ticket_date_booked_alter_ticket_payment_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='event',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='num_of_person',
        ),
        migrations.AddField(
            model_name='ticket',
            name='booking',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='eventbooking.booking'),
        ),
    ]