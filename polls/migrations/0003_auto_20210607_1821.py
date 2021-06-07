# Generated by Django 3.2.4 on 2021-06-07 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20210607_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='user_id',
        ),
        migrations.CreateModel(
            name='UserPoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_polls', to='polls.poll')),
            ],
            options={
                'unique_together': {('user_id', 'poll')},
            },
        ),
    ]
