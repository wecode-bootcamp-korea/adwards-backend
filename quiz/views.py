import json

from .models        import Question, Choices, Answer
from user.utils     import user_login_required, advertiser_login_required

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

                if len(quiz['answer']) > 1:
                    answers = [
                        Answer(
                            question   = created_quiz, 
                            choices_id = answer
                        )
                        for answer in quiz['answer']
                    ]
                    Answer.objects.bulk_create(answers)
                else:
                    answer_choice_id = Choices.objects.get(question = created_quiz, content = quiz['answer'][0])
                    Answer.objects.create(question = created_quiz, choices = answer_choice_id)
                    
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"ERROR":"MISSING_DATA"}, status=400)
