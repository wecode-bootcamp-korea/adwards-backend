from django.db import models
from advertisement.models import *

class QuestionType(models.Model):
    #field_value = [short_answer, multi_choices]
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'question_type'
    
class AnswerType(models.Model):
    #field_value = [single_answer, multi_answer]
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'answer_type'

class Question(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    question_type = models.ForeignKey(QuestionType, on_delete=models.SET_NULL, null=True)
    answer_type = models.ForeignKey(AnswerType, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=2500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'questions'

class Choices(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'choices'

class Answer(models.Model):
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questions_set')
    choices = models.ForeignKey(Choices, on_delete=models.CASCADE, related_name='choices_set')

    class Meta:
        db_table = 'answers'

