# Generated by Django 2.0.5 on 2018-06-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoinsee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrativeentity',
            name='entity_type',
            field=models.CharField(choices=[('township', 'Township'), ('scot', 'SCOT'), ('epci', 'EPCI'), ('county', 'County'), ('region', 'Region'), ('state', 'State'), ('country', 'Country')], default='county', help_text='Administrative area type', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='administrativeentity',
            name='insee',
            field=models.CharField(help_text='Insee Code', max_length=5),
        ),
        migrations.AlterUniqueTogether(
            name='administrativeentity',
            unique_together={('insee', 'entity_type')},
        ),
    ]