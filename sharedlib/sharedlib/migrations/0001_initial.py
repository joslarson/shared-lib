# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField(max_length=4)),
                ('is_explicit', models.BooleanField(default=False)),
                ('external_link', models.TextField()),
                ('image_url', models.TextField()),
                ('vote_count', models.IntegerField(default=1)),
                ('cost', models.IntegerField(null=True, blank=True)),
                ('file_url', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(related_name=b'profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('album', models.ForeignKey(related_name=b'votes', to='sharedlib.Album')),
                ('user', models.ForeignKey(related_name=b'votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'album')]),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(related_name=b'albums', to='sharedlib.Artist'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='purchaser',
            field=models.ForeignKey(related_name=b'purchased_albums', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='suggester',
            field=models.ForeignKey(related_name=b'suggested_albums', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
