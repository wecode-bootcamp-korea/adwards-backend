import json
import bcrypt
import jwt

from django.test import TestCase, Client

from user.models import *
from user.views import *
from .models import *
from .views import *
from adwards.settings import SECRET_KEY


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

class AdvertiserSigninTest(TestCase):
    def setUp(self):
        industry = IndustryType.objects.create(id=1, name="교육사업")
        bytes_pw = bytes('12341234', 'utf-8')
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
        
        advertiser = Advertiser.objects.create(
            id                      = 1,
            email                   = 'wecode@grace.co',
            password                = hashed_pw.decode('utf-8'),
            company_name            = 'wecode',
            balance                 = '1000000',
            business_license_number = '10-345630291-01',
            industry_type           = industry,
            contact                 = '010-0000-0000',
            company_address         = '서울특별시 강남구 삼성동 테헤란로 427',
            company_description     = '3개월만에 개발자! 될 수 있습니다. 코딩부트캠프 wecode!',
            homepage                = 'https://wecode.co.kr',
            thumbnail               = 'https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/landing/bootcamp/boot_4.jpg',
        )
    
    def test_advertiser_signin_positive(self):
        c = Client()
        
        test = {
            'email':'wecode@grace.co',
            'password':'12341234'
        }

        response = c.post("/signin/advertiser", json.dumps(test), **{"content_type":"application/json"})
        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(response.json(),
                         {
                         "access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
                         eyJlbWFpbCI6IndlY29kZUBncmFjZSIsInVzZXJfdHlwZSI6ImFkd\
                         mVydGlzZSIsImV4cCI6IjEyMzQ1NjciLCJpYXQiOiIxMjM0NTY3In0\
                         .NzKTYzWesOvotb-6QTBIsXMevdMq1uUHutjohGcJNKE"
                        }
        )
    
    def test_advertiser_signin_negative(self):
        c = Client()
        
        test = {
            'email':'wecode@grace',
            'password':'12341234'
        }

        response = c.post("/signin/advertiser", json.dumps(test), **{"content_type":"application/json"})
        self.assertEqual(response.status_code, 401)

class UserSigninTest(TestCase):
    def setUp(self):
        state      = State.objects.create(id = 1, name = "서울")
        gender     = Gender.objects.create(id = 1, name = "남자")
        bank       = Bank.objects.create(id = 1, name = "우리은행")
        bytes_pw   = bytes('12345678', 'utf-8')
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

    def test_user_signin_positive(self):
        c = Client()
        
        test = {
            'email':'mail@mail.com',
            'password': '12345678'
        }

        response = c.post("/signin/user", json.dumps(test), **{"content_type":"application/json"})
        print(response.json())
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.json(),
                         {
                         "access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
                         eyJlbWFpbCI6IndlY29kZUBncmFjZSIsInVzZXJfdHlwZSI6ImFkd\
                         mVydGlzZSIsImV4cCI6IjEyMzQ1NjciLCJpYXQiOiIxMjM0NTY3In0\
                         .NzKTYzWesOvotb-6QTBIsXMevdMq1uUHutjohGcJNKE"
                        }
        )
 
    def test_user_signin_negative(self):
        c = Client()
        
        test = {
            'email':'mail@grace',
            'password':'12345678'
        }

        response = c.post("/signin/user", json.dumps(test), **{"content_type":"application/json"})
        self.assertEqual(response.status_code, 401) 
