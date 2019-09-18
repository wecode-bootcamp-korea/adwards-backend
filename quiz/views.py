from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import *
from advertisement.models import Advertisement
from user.utils import *

import json

class QuizCreateView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
             
            Question.objects.create(
                    advertisement_id=data['ad_id'],
                    question_type_id=data['quest_id'],
                    answer_type_id=data['answer_id'],
                    answer=data['answer'],
                    choices=data['choices'],
                    title=data['title'],
                    content=data['content'],
                    )

            return HttpResponse(status=200)
        except TypeError:
            return HttpResponse(status=400)
        except KeyError:
            return HttpResponse(status=400)
        except ValueError:
            return HttpResponse(status=400)
        except Advertisement.DoesNotExist:
            return HttpResponse(status=404)
        except Question.DoesNotExist:
            return HttpResponse(status=404)

            

        


