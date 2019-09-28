import json

from advertisement.models import QuizHistory, Advertisement
from .models              import Question, Choices, Answer
from user.utils           import user_login_required, advertiser_login_required

from django.views       import View
from django.http        import HttpResponse, JsonResponse

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
                        questions = created_quiz, 
                        content__in = quiz["answers"]
                    )
                    answers = [
                        Answer(
                            questions = created_quiz, 
                            choices  = answer
                        )
                        for answer in answer_choice_ids
                    ]
                    Answer.objects.bulk_create(answers)
                else:
                    answer_choice_id = Choices.objects.get(question = created_quiz, content = quiz['answers'][0])
                    Answer.objects.create(questions = created_quiz, choices = answer_choice_id)
                    
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"ERROR":"MISSING_DATA"}, status=400)

class QuizCorrectView(View):
    @user_login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            for user_answer in data["user_answers"]:
                question_id = user_answer['quiz_id']
                user_answers = user_answer['answers']

                answers = Question.objects.get(id = question_id).questions_set.values_list('choices_id', flat = True)

                if set(user_answers) != set(answers):
                    return JsonResponse({"message":False}, status=200)
                
            QuizHistory.objects.create(user = request.user, advertisement_id = data['ad_id'])
            return JsonResponse({"message":True}, status=200)
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

class QuizHistoryListView(View):
        @user_login_required
        def get(self, request):
            offset = int(request.GET.get('offset',0))
            limit  = int(request.GET.get('limit', 10))
            
            quiz_history_list = QuizHistory.objects.select_related('advertisement').filter(user = request.user)
            quiz_reward = quiz_history_list.aggregate(reward = Sum("advertisement__price_per_view"))
            history_data = [
                {
                'id'            :quiz_history.id,
                'ad_id'         :quiz_history.advertisement_id,
                'ad_title'      :quiz_history.advertisement.title,
                'ad_price_view' :quiz_history.advertisement.price_per_view,
                'created_at'    :quiz_history.created_at
                }
                for quiz_history in quiz_history_list.order_by('-created_at')[offset:limit]
            ] 
                
            return JsonResponse({
                "quiz_history":history_data, 
                "reward_point":quiz_reward["reward"], 
                "total_count":quiz_history_list.count()
            })

class QuizChartDataView(View):
        @advertiser_login_required
        def get(self, request, ad_id): 
            quiz_history_data = QuizHistory.objects.select_related('user').filter(advertisement_id = ad_id)

            if quiz_history_data.filter(user__gender = 1).count() != 0 and quiz_history_data.filter(user__gender = 2).count() != 0:
                male_count = quiz_history_data.filter(user__gender = 1).count()
                female_count = quiz_history_data.filter(user__gender = 2).count()
                total_count = male_count + female_count
                male_ratio = round(male_count/(total_count)*100.0, 2)
                female_ratio = round(female_count/(total_count)*100.0, 2)

                donut_chart_data = [['남성', male_ratio],['여성', female_ratio]]
            else:
                donut_chart_data = [['남성', 50],['여성', 50]]

            age_range = quiz_history_data.values_list('user__age', flat=True).order_by('user__age')
            stack_chart_data = {'0~20':0, '21~30':0, '31~40':0, '41~50':0, '51~60':0, '61~70':0}

            for age in age_range:
                if age <= 20:
                    stack_chart_data['0~20'] += 1
                elif 20 < age <= 30:
                    stack_chart_data['21~30'] += 1
                elif 30 < age <= 40:
                    stack_chart_data['31~40'] += 1
                elif 40 < age <= 50:
                    stack_chart_data['41~50'] += 1
                elif 50 < age <= 60:
                    stack_chart_data['51~60'] += 1
                else:
                    stack_chart_data['61~70'] += 1

            return JsonResponse({
                "donut_stack_chart_data":donut_chart_data,
                "stack_chart_data":{
                                    "key":list(stack_chart_data.keys()),
                                    "values":list(stack_chart_data.values())
                                   }
                })
