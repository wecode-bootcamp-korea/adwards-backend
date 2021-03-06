# Generated by Django 2.2.4 on 2019-09-26 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('advertisement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'answer_type',
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'question_type',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=2500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, null=True)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.Advertisement')),
                ('answer_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.AnswerType')),
                ('question_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.QuestionType')),
            ],
            options={
                'db_table': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Question')),
            ],
            options={
                'db_table': 'choices',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choices', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices_set', to='quiz.Choices')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_set', to='quiz.Question')),
            ],
            options={
                'db_table': 'answers',
            },
        ),
    ]
