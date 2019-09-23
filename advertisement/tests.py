import json
from django.test import TestCase, Client
import jwt 
from adwards.settings import SECRET_KEY

from user.models import *
from user.views import *
from .models import *
from .views import *

class AdvertisementTest(TestCase):
    def setUp(self): 
        industry = IndustryType.objects.create(id=1, name="컴퓨터")

        advertiser = Advertiser.objects.create(
            company_name=            "한바름",
            business_license_number= 12341234,
            email=                   "mail@mail.com",
            password=                "12345678",
            industry_type=           industry,
            contact=                 '01012341234',
            thumbnail=               "https://www.notion.so/Django-test-py-8e2b1605e5864357bcd05971f23f686d",
            homepage=                "https://www.notion.so/Django-test-py-8e2b1605e5864357bcd05971f23f686d",
            company_address=         "서울서울서울",
            company_description=     "한바름",
             )

        state      = State.objects.create(id=1, name="서울")
        gender     = Gender.objects.create(id=1, name="남자")
        interests1 = InterestsType.objects.create(id=1, name="코딩")
        interests2 = InterestsType.objects.create(id=2, name="컴퓨터")
        interests3 = InterestsType.objects.create(id=3, name='위워크')
        interests4 = InterestsType.objects.create(id=4, name="위코드")
        bank       = Bank.objects.create(id=1, name="우리은행")

        user = User.objects.create(
            user_name=      "한바름",
            nickname=       "별명",
            email=          "mail@mail.com",
            password=       "12345678",
            age=            30,
            state=       state,
            gender=      gender,
            cellphone=      '01012341234',
            thumbnail=      "https://www.notion.so/Django-test-py-8e2b1605e5864357bcd05971f23f686d",
            bank=        bank,
            account_owner=  "한바름",
            account_number= "010010010",
            )
        user.interests.add(interests1)
        
        ad_cate = AdvertisementCategory.objects.create(id=1, name='컴퓨터')
        ad_tag = Tag.objects.create(id=1, name='개발') 
        
        ad = Advertisement.objects.create(
                id             = 1,
                title          = '테스트 입니다',
                advertiser     = advertiser, 
                description    = '안녕하세요 안녕하세요 안녕하세요',
                video_link     = 'hhhhhhhhhhhhhhh',
                thumbnail      = 'nnnnnnnnnnnnn',
                budget         = 100000,
                price_per_view = 500,
                ad_category    = ad_cate,
                like_count     = 100,
                quiz_count     = 100,
                )
        ad.tag.add(ad_tag)
        ad.interests.add(interests1)
        
    def test_advertisement_create(self):
        advertiser_payload = {
                "user_email": "mail@mail.com",
                "user_type":  "advertiser"
                }
        Authorization_advertiser = jwt.encode(advertiser_payload, SECRET_KEY, "HS256").decode('utf-8')

        c = Client() 
        
        test = {
                'title':                 '테스트테스트',
                'description':           '안녕하세요 안녕하세요 안녕하세요',
                'ad_category_id':        1,
                'video_link':            'hhhhhhhhhhhhhhhhhh',
                'thumbnail':             'nnnnnnnnnnnnn',
                'budget':                5000000,
                'price_per_view':        500,
                'tag':                   ['컴퓨터','개발'],
                'interests_type_id':     [1,2,3]
                }

        response = c.post("/advertisement", json.dumps(test), 
                **{"HTTP_Authorization": Authorization_advertiser,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                response.json(),
                {
                    "advertisement_id":  2
                    }
                )

    def test_get_advertisement_list_by_condition(self):
        c = Client()
        user_payload = {
                "user_email": "mail@mail.com",
                "user_type":  "user"
                }
        Authorization_user = jwt.encode(user_payload, SECRET_KEY, "HS256").decode('utf-8')
        
        advertiser_payload = {
                "user_email": "mail@mail.com",
                "user_type":  "advertiser"
                }
        Authorization_advertiser = jwt.encode(advertiser_payload, SECRET_KEY, "HS256").decode('utf-8')

        response = c.get("/advertisement?offset=0&limit=10&advertiser",
                **{"HTTP_Authorization": Authorization_advertiser,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
        
        response = c.get("/advertisement?offset=0&limit=10&interests=set",
                 **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
        
        response = c.get("/advertisement?offset=0&limit=10&category_id=1",
                **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
         
        response = c.get("/advertisement?offset=0&limit=10&price_per_view=set",
                **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
         
        response = c.get("/advertisement?offset=0&limit=10&like=set",
                **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
         
        response = c.get("/advertisement?offset=0&limit=10&tag=개발",
                **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
