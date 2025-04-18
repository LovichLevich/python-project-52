# Generated by Django 5.1.7 on 2025-04-13 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0003_alter_labels_author'),
        ('tasks', '0003_rename_label_task_labels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='labels',
        ),
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='labels.labels', verbose_name='Labels'),
        ),
    ]
