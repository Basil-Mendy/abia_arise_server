# Generated migration for adding PIN reset fields to IndividualMember

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_progroup_country_progroup_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualmember',
            name='pending_reset_pin',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='individualmember',
            name='pending_reset_pin_otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='individualmember',
            name='pending_reset_pin_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
