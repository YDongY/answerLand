# Generated by Django 3.0.8 on 2020-07-20 14:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('uuid_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='内容')),
                ('reply', models.BooleanField(default=False, verbose_name='是否评论')),
            ],
            options={
                'verbose_name': '首页',
                'verbose_name_plural': '首页',
                'ordering': ('-create_time',),
            },
        ),
    ]
