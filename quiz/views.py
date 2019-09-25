import json

from advertisement.models import QuizHistory, Advertisement
from .models              import Question, Choices, Answer
from user.utils           import user_login_required, advertiser_login_required

from django.views   import View
from django.http    import HttpResponse, JsonResponse

class QuizView(View): 
    @advertiser_login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            for quiz in data['quizzes']:
                created_quiz = Question.objects.create(
                    advertisement_id  = data['ad_id'],
                    question_type_id  = 2,
                    answer_type_id    = 2,
                    title             = quiz['title'],
                    content           = quiz['content'],
                )

                choices = [
                    Choices(
                        question = created_quiz, 
                        content  = content
                    ) 
                    for content in quiz['choices']
                ]
                Choices.objects.bulk_create(choices)

                if len(quiz['answers']) > 1:
                    answer_choice_ids = Choices.objects.filter(
                        question = created_quiz, 
                        content__in = quiz["answers"]
                    )
                    answers = [
                        Answer(
                            question = created_quiz, 
                            choices  = answer
                        )
                        for answer in answer_choice_ids
                    ]
                    Answer.objects.bulk_create(answers)
                else:
                    answer_choice_id = Choices.objects.get(question = created_quiz, content = quiz['answers'][0])
                    Answer.objects.create(question = created_quiz, choices = answer_choice_id)
                    
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"ERROR":"MISSING_DATA"}, status=400)

class QuizCorrectView(View):
    @user_login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            for user_answer in data["user_answers"]:
                correct_status = []
                question_id = user_answer['quiz_id']
                user_answers = user_answer['answers']

                question_answer = Question.objects.get(id = question_id).questions_set.values_list('choices_id')
                answers  = [question[0]  for question in question_answer]                

                if set(user_answers) == set(answers):
                    correct_status.append(True)
                else:
                    correct_status.append(False)

            if all(correct_status):
                QuizHistory.objects.create(user = request.user, advertisement_id = data['ad_id'])
                return JsonResponse({"message":True}, status=200)
            else:
                return JsonResponse({"message":False}, status=200)
        except KeyError:
            return JsonResponse({"ERROR":"MISSING_DATA"}, status=400)

class QuizListView(View):
    def get(self, request, ad_id):
        questions = Question.objects.prefetch_related('choices_set').filter(advertisement_id = ad_id)
        choices_list = [question.choices_set.all() for question in questions]
           
        quizzes = [{
            'question'      : question.title,
            'content'       : question.content,
            'answer_type'   : question.answer_type.name,
            'question_type' : question.question_type.name,
            'created_at'    : question.created_at,
            'choices'       : [{"id": choice.pk, "content": choice.content} for choice in choices]
        } for question, choices in zip(questions, choices_list)]

        return JsonResponse(quizzes, safe=False, status = 200) 
