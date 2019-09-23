import json
from django.test import TestCase, Client

from user.models import *
from user.views import *
from .models import *
from .views import *


class AdvertiserSignupTest(TestCase):
    def setUp(self):
        industry = IndustryType.objects.create(id=1, name="컴퓨터")

    def test_advertiser_signup(self):
        c = Client()

        test = {
            'company_name': "한바름",
            'business_license_number':12341234,
            'email': "mail@mail.com",
            'password': "12345678",
            'industry_type_id':1,
            'contact':'01012341234',
            'thumbnail':"https://www.notion.so/Django-test-py-8e2b1605e5864357bcd05971f23f686d",
            'homepage':"https://www.notion.so/Django-test-py-8e2b1605e5864357bcd05971f23f686d",
            'company_address':"서울서울서울",
            'company_description': "한바름",
        }

        response = c.post("/signup/advertiser", json.dumps(test), **{"content_type":"application/json"})
        self.assertEqual(response.status_code, 200)
    
class SignupTest(TestCase):
    def setUp(self):
        state = State.objects.create(id=1, name="서울")
        gender = Gender.objects.create(id=1, name="남자")
        interests = InterestsType.objects.create( id=1, name="코딩")
        interests2 = InterestsType.objects.create(id=2, name="컴퓨터")
        interests3 = InterestsType.objects.create(id=3, name='위워크')
        interests4 = InterestsType.objects.create(id=4, name="위코드")
        bank = Bank.objects.create(id=1, name="우리은행")

    def test_user_signup(self):
        c = Client()

        test = {
            'user_name': "한바름",
            'nickname':"별명",
            'email': "mail@mail.com",
            'password': "12345678",
            'age':30,
            'state_id':1,
            'gender_id':1,
            'cellphone':'01012341234',
            'thumbnail':"https://www.notion.so/Django-test-py-8e2b1605e5864357bcd05971f23f686d",
            'bank_id':1,
            'account_owner': "한바름",
            'account_number': "010010010",
            'interests': [1, 2, 3, 4]
        }

        response = c.post("/signup/user", json.dumps(test), content_type= "application/json")  
        print(response) 
        self.assertEqual(response.status_code, 200)
