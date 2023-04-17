# Generated by Django 4.1 on 2022-10-15 20:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TweetDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweetID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('message', models.CharField(max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HomePage.basicuserdb')),
            ],
        ),
    ]