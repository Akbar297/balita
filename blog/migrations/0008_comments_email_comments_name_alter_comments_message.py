# Generated by Django 5.0.2 on 2024-03-07 15:19

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_rename_comment_comments_message_contact_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='comments',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='message',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
