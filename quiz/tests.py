import json
import bcrypt
import jwt
from pprint import pprint

from .views                 import *
from advertisement.models   import *
from quiz.models            import *
from user.models            import *
from adwards.settings       import SECRET_KEY

from django.test            import TestCase, Client

class QuizModelTest(TestCase):
    def setUp(self):
        industry_type = IndustryType.objects.create(
                id=1,
                name='교육사업'
                )
        ad_category = AdvertisementCategory.objects.create(
                id=1,
                name='교육'
                )
        tag = Tag.objects.create(
                id=1,
                name='coding bootcamp'
                )
        bytes_pw = bytes('1234', 'utf-8')
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
        advertiser = Advertiser.objects.create(
                id=1,
                email='wecode@grace.co',
                password=hashed_pw.decode('utf-8'),
                company_name='wecode',
                balance='1000000',
                business_license_number='10-345630291-01',
                industry_type=industry_type,
                contact='010-0000-0000',
                company_address='서울특별시 강남구 삼성동 테헤란로 427',
                company_description='3개월만에 개발자! 될 수 있습니다. 코딩부트캠프 wecode!',
                homepage='https://wecode.co.kr',
                thumbnail='https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/landing/bootcamp/boot_4.jpg',
                )
        advertisement = Advertisement.objects.create(
                id=1,
                title='3개월만에 개발자?',
                description='개발자가 되는 가장 빠른 길, wecode!',
                advertiser=advertiser,
                ad_category=ad_category,
                video_link='https://youtu.be/h_XWL253eEY',
                budget='100000',
                price_per_view='100',
                switch=True
                )
        advertisement_tag = AdvertisementTag(
                id=1,
                advertisement=advertisement,
                tag=tag
                )
        question_type = QuestionType.objects.create(
                id=2,
                name='multi_choices'
                )
        answer_type = AnswerType.objects.create(
                id=2,
                name='multi_answer'
                )
        questions = Question.objects.create(
                id = 1,
                advertisement = advertisement,
                question_type = question_type,
                answer_type = answer_type,
                title = '위코드',
                content = '현재 교육중인 기수는 3기다.'
                )
        questions_2 = Question.objects.create(
                id = 2,
                advertisement = advertisement,
                question_type = question_type,
                answer_type = answer_type,
                title = '위코드',
                content = '현재 교육중인 기수는 몇명일까요?'
                )
        choices_1 = Choices.objects.create(
                id = 1,
                question = questions,
                content = 'o'
                )
        choices_2 = Choices.objects.create(
                id = 2,
                question = questions,
                content = 'x'
                )
        choices_3 = Choices.objects.create(
                id = 3,
                question = questions_2,
                content = '12'
                )
        choices_4 = Choices.objects.create(
                id = 4,
                question = questions_2,
                content = '15'
                )
        choices_5 = Choices.objects.create(
                id = 5,
                question = questions_2,
                content = '20'
                )
        choices_6 = Choices.objects.create(
                id = 6,
                question = questions_2,
                content = '21'
        )

        answer  = Answer.objects.create(questions = questions, choices_id=1)
        answers = [
            Answer(questions = questions_2, choices_id=choice)
            for choice in [3, 4]
        ]
        answer_2 = Answer.objects.bulk_create(answers)
        
        state      = State.objects.create(id = 1, name = "서울")
        gender     = Gender.objects.create(id = 1, name = "남자")
        bank       = Bank.objects.create(id = 1, name = "우리은행")
        bytes_pw   = bytes('1234', 'utf-8')
        hashed_pw  = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
        user = User.objects.create(
            id             = 1,
            user_name      = "한바름",
            nickname       = "별명",
            email          = "mail@mail.com",
            password       = hashed_pw.decode('utf-8'),
            age            = 30,
            state_id       = 1,
            gender_id      = 1,
            cellphone      = '01012341234',
            thumbnail      = "https://www.notion.so/Django-test-py-8e2b1605e5864357bcd05971f23f686d",
            bank_id        = 1,
            account_owner  = "한바름",
            account_number = "010010010",
        )
        interests = [
            InterestsType(pk = id, name = interest)
            for id, interest in zip(range(1,4), ['코딩','컴퓨터', '위워크', '위코드'])
        ]
        InterestsType.objects.bulk_create(interests)
        for interest in interests:
            user.interests.add(interest)
    
    def test_question_create_view_positive(self):
        c = Client()
        
        login_test = {
            "email":"wecode@grace.co",
            "password":"1234"
        }

        test = {
                "ad_id":1,
                "quizzes":
                [
                    {
                        'title':'hello_wecode',
                        'content':'wecode는 현재 교육중인 기수는 3기이다.',
                        'choices':['o','x'],
                        'answers':['o']
                    }
                ]
        }

        login_response = c.post("/signin/advertiser", data=json.dumps(login_test), content_type="application/json")
        access_token = login_response.json()["access_token"]
        response = c.post("/quiz", data=json.dumps(test), HTTP_AUTHORIZATION=access_token, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_question_create_view_negative(self):
        c = Client()
        
        login_test = {
            "email":"wecode@grace.co",
            "password":"1234"
        }

        test = {
                "ad_id":1,
                "quizzes":
                [
                    {
                        'title':'hello_wecode',
                        'content':'wecode는 현재 교육중인 기수는 3기이다.',
                        'choices':['o','x'],
                        'answers':['o']
                    },
                    {
                        'title':'hello_wecode',
                        'content':'wecode는 현재 교육중인 기수는 3기이다.',
                        'choices':['o','x'],
                        'answers':['o']
                    }
                ]
        }

        login_response = c.post("/signin/advertiser", data=json.dumps(login_test), content_type="application/json")
        access_token = login_response.json()["access_token"]
        response = c.post("/quiz", data=json.dumps(test), HTTP_AUTHORIZATION=access_token, content_type='application/json')
        self.assertEqual(response.status_code, 200) 

    def test_question_correct_view_positive(self):
        c = Client()
        
        login_test = {
            "email":"mail@mail.com",
            "password":"1234"
        }

        test = {
                "ad_id":1,
                "user_answers": [
                                {"quiz_id": 1, "answers": [1]},
                                {"quiz_id": 2, "answers": [3,4]}
                               ]
        }
        
        login_response = c.post("/signin/user", data=json.dumps(login_test), content_type="application/json")
        access_token = login_response.json()["access_token"]
        response = c.post("/quiz/answer", data=json.dumps(test), HTTP_AUTHORIZATION=access_token, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message":True})
    
    def test_question_correct_view_negaitive(self):
        c = Client()
        
        login_test = {
            "email":"mail@mail.com",
            "password":"1234"
        }

        test = {
                "ad_id":1,
                "user_answers": [
                                {"quiz_id": 1, "answers": [1]},
                                {"quiz_id": 2, "answers": [3,4,5]}
                               ]
        }

        login_response = c.post("/signin/user", data=json.dumps(login_test), content_type="application/json")
        access_token = login_response.json()["access_token"]
        response = c.post("/quiz/answer", data=json.dumps(test), HTTP_AUTHORIZATION=access_token, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message":False})

    def test_question_list_view_positive(self):
        c = Client()

        response = c.get("/advertisement/1/quiz", content_type='application/json')
        pprint(response.json())
        self.assertEqual(response.status_code, 200)

    def test_question_list_view_negative(self):
        c = Client()

        response = c.get("/advertisement/10/quiz", content_type='application/json')
        pprint(response.json())
        self.assertEqual(response.json(), [])
    
    def test_question_history_list_view(self):
        c = Client()
        
        login_test = {
            "email":"mail@mail.com",
            "password":"1234"
        }

        test = {
                "ad_id":1,
                "user_answers": [
                                {"quiz_id": 1, "answers": [1]},
                                {"quiz_id": 2, "answers": [3,4]}
                               ]
        }
        
        login_response = c.post("/signin/user", data=json.dumps(login_test), content_type="application/json")
        access_token = login_response.json()["access_token"]
        correct_response = c.post("/quiz/answer", data=json.dumps(test), HTTP_AUTHORIZATION=access_token, content_type='application/json')
        response = c.get("/quiz/history?offset=0&limit=10", HTTP_AUTHORIZATION=access_token, content_type = "application/json")

    def test_question_donut_chart_view(self):
        c = Client()
        
        user_login_test = {
            "email":"mail@mail.com",
            "password":"1234"
        }

        advertiser_login_test = {
            "email":"wecode@grace.co",
            "password":"1234"
        }

        test = {
                "ad_id":1,
                "user_answers": [
                                {"quiz_id": 1, "answers": [1]},
                                {"quiz_id": 2, "answers": [3,4]}
                               ]
        }
        
        login_response = c.post("/signin/user", data=json.dumps(user_login_test), content_type="application/json")
        access_token = login_response.json()["access_token"]
        c.post("/quiz/answer", data=json.dumps(test), HTTP_AUTHORIZATION=access_token, content_type='application/json')
        login_response = c.post("/signin/advertiser", data=json.dumps(advertiser_login_test), content_type="application/json")
        access_token = login_response.json()["access_token"] 
        response = c.get("/advertisement/1/chart", HTTP_AUTHORIZATION=access_token, content_type='application/json')
        print(response.json())
