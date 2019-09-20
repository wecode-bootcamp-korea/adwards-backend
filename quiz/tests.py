import json
import bcrypt
import jwt

from .views                 import *
from advertisement.models   import *
from quiz.models            import *
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
                password=hashed_pw,
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

    def test_question_create_view_positive(self):
        c = Client()

        test = {
                "ad_id":1,
                'title':'hello_wecode',
                'content':'wecode는 현재 교육중인 기수는 3기이다.',
                'choices':['o','x'],
                'answer':['o']
                }

        access_token = jwt.encode(
                {'user_id':'wecode@grace.co', 'user_type':'advertiser'},
                SECRET_KEY,
                'HS256'
                )

        response = c.post("/quiz", data=json.dumps(test), HTTP_AUTHORIZATION=access_token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_question_create_view_except(self):
            c = Client()

            test = {
                    "ad_id":1,
                    'title':'hello_wecode',
                    'content':'wecode는 몇명의 멘토들이 있을까요?',
                    'choices':['2','3','4','5'],
                    'answer':['3']
                    }

            access_token = jwt.encode(
                    {'user_id':'wecode@grace.co', 'user_type':'user'},
                    SECRET_KEY,
                    'HS256'
                    )

            response = c.post("/quiz", data=json.dumps(test), HTTP_AUTHORIZATION=access_token, content_type='application/json')
            self.assertEqual(response.status_code, 401)    
