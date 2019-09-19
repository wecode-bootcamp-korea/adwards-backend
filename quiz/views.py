import json

from .models        import Question
from user.utils     import user_login_required, advertiser_login_required

from django.views   import View
from django.http    import HttpResponse, JsonResponse

class QuizView(View):
    
    @advertiser_login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
    
            Question.objects.create(
                    advertisement_id=data['ad_id'],
                    question_type_id=2,
                    answer_type_id=2,
                    answer=data['answer'],
                    choices=data['choices'],
                    title=data['title'],
                    content=data['content'],
                    )

            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"ERROR":"MISSING_DATA"}, status=400)
