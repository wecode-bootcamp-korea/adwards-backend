import json

from .models        import Question, Choices, Answer
from user.utils     import user_login_required, advertiser_login_required

from django.views   import View
from django.http    import HttpResponse, JsonResponse

class QuizView(View): 
    @advertiser_login_required
    def post(self, request):
        try:
            reqst = json.loads(request.body)
    
            quiz = Question.objects.create(
                    advertisement_id  = reqst['ad_id'],
                    question_type_id  = 2,
                    answer_type_id    = 2,
                    title             = reqst['title'],
                    content           = reqst['content'],
                    )

            choices = [
                Choices(
                    question = quiz, 
                    content  = content
                ) 
                for content in reqst['choices']
            ]
            Choices.objects.bulk_create(choices)

            if len(reqst['answer']) > 1:
                answers = [
                    Answer(
                        question   = quiz, 
                        choices_id = answer
                    )
                    for answer in reqst['answer']
                ]
                Answer.objects.bulk_create(answers)

            answer_choice_id = Choices.objects.get(question = quiz, content = reqst['answer'][0])
            Answer.objects.create(question = quiz, choices = answer_choice_id)

            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"ERROR":"MISSING_DATA"}, status=400)
