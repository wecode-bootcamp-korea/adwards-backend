from django.test import TestCase, Client
from .views import *
from advertisement.models import *
from quiz.models import *

import json

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
        advertiser = Advertiser.objects.create(
                id=1,
                email='wecode@grace.co',
                password='12341234',
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
                id=1,
                name='multi_choices'
                )

        answer_type = AnswerType.objects.create(
                id=1,
                name='multi_answer'
                )

    def test_question_create_view_positive(self):
        c = Client()

        test = {
                "ad_id":1,
                'quest_id':1,
                'answer_id':1,
                'answer':['o'],
                'title':'hello_wecode',
                'content':'wecode는 현재 교육중인 기수는 3기이다.',
                'choices':['o','x']
                }

        response = c.post("/quiz", data=json.dumps(test), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_question_create_view_negative(self):
            c = Client()

            test = {
                    "ad_id":'asds',
                    'quest_id':'asdas',
                    'answer_id':1,
                    'answer':['o'],
                    'title':'hello_wecode',
                    'content':'wecode는 현재 교육중인 기수는 3기이다.',
                    'choices':['o','x']
                    }

            response = c.post("/quiz", data=json.dumps(test), content_type='application/json')
            self.assertEqual(response.status_code, 400)
    
    def test_question_create_view_except_case1(self):
        c = Client()

        test = {
                'quest_id':1,
                'answer_id':1,
                'answer':['o'],
                'title':'hello_wecode',
                'content':'wecode는 현재 교육중인 기수는 3기이다.',
                }

        response = c.post("/quiz", data=json.dumps(test), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
    def test_question_create_view_except_case2(self):
        c = Client()

        test = [{
                'quest_id':1,
                'answer_id':1,
                'answer':['o'],
                'title':'hello_wecode',
                'content':'wecode는 현재 교육중인 기수는 3기이다.',
                }]

        response = c.post("/quiz", data=json.dumps(test), content_type='application/json')
        self.assertEqual(response.status_code, 400)





