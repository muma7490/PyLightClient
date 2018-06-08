# Generated by Django 2.0.6 on 2018-06-08 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client_settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientName', models.CharField(max_length=255, verbose_name='Name of the pi client')),
                ('serverAddress', models.CharField(max_length=255, verbose_name='Address of the server that set the ip of the pi')),
            ],
        ),
        migrations.CreateModel(
            name='IOs',
            fields=[
                ('ioNr', models.IntegerField(primary_key=True, serialize=False, verbose_name='physical io nr on pi')),
            ],
        ),
        migrations.CreateModel(
            name='UsedIOs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='human readable name for the io')),
                ('active', models.BooleanField(default=False, verbose_name='Active/Non Active IO')),
            ],
        ),
        migrations.AddField(
            model_name='ios',
            name='usedIOId',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PyLightORM.UsedIOs', verbose_name='link to the used ios'),
        ),
    ]