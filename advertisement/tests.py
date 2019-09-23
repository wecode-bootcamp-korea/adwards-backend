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
            thumbnail = "https://www.notion.so/Django-test-py-8e2b1605e5864357bcd05971f23f686d",
            homepage  = "https://www.notion.so/Django-test-py-8e2b1605e5864357bcd05971f23f686d",
            company_address=         "서울서울서울",
            company_description=     "한바름",
             )

        state      = State.objects.create(id=1, name="서울")
        gender     = Gender.objects.create(id=1, name="남자")

        interests1 = InterestsType.objects.create(id=1, name="inter1")
        interests2 = InterestsType.objects.create(id=2, name="inter2")
        interests3 = InterestsType.objects.create(id=3, name="inter3")
        interests4 = InterestsType.objects.create(id=4, name="inter4")
        interests5 = InterestsType.objects.create(id=5, name="inter5")
        interests6 = InterestsType.objects.create(id=6, name="inter6")

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
        user.interests.add(interests2)
        user.interests.add(interests3)
        user.interests.add(interests4)
        
        ad_cate1 = AdvertisementCategory.objects.create(id=1, name='컴퓨터1')
        ad_tag1 = Tag.objects.create(id=1, name='개발1') 
        
        ad1 = Advertisement.objects.create(
                id             = 1,
                title          = "title1",
                advertiser     = advertiser, 
                description    = "description1",
                video_link     = 'video_link1',
                thumbnail      = 'thumbnail1',
                budget         = 10000000,
                price_per_view = 100,
                ad_category    = ad_cate1,
                like_count     = 100,
                quiz_count     = 100,
                switch = True,
                )
        ad1.tag.add(ad_tag1)
        ad1.interests.add(interests1)
                
        ad_cate2 = AdvertisementCategory.objects.create(id=2, name='컴퓨터2')
        ad_tag2 = Tag.objects.create(id=2, name='개발2') 
        
        ad2 = Advertisement.objects.create(
                id             = 2,
                title          = "title2",
                advertiser     = advertiser, 
                description    = "description2",
                video_link     = 'video_link2',
                thumbnail      = 'thumbnail2',
                budget         = 20000000,
                price_per_view = 200,
                ad_category    = ad_cate2,
                like_count     = 200,
                quiz_count     = 200,
                switch = True,
                deleted=True,
                )
        ad2.tag.add(ad_tag2)
        ad2.interests.add(interests2)
                
        ad_cate3 = AdvertisementCategory.objects.create(id=3, name='컴퓨터3')
        ad_tag3 = Tag.objects.create(id=3, name='개발3') 
        
        ad3 = Advertisement.objects.create(
                id             = 3,
                title          = "title3",
                advertiser     = advertiser, 
                description    = "description3",
                video_link     = 'video_link3',
                thumbnail      = 'thumbnail3',
                budget         = 30000000,
                price_per_view = 300,
                ad_category    = ad_cate3,
                like_count     = 300,
                quiz_count     = 300,
                switch = True,
                )
        ad3.tag.add(ad_tag3)
        ad3.interests.add(interests3)
         
        ad_cate4 = AdvertisementCategory.objects.create(id=4, name='컴퓨터4')
        ad_tag4 = Tag.objects.create(id=4, name='개발4') 
        
        ad4 = Advertisement.objects.create(
                id             = 4,
                title          = "title4",
                advertiser     = advertiser, 
                description    = "description4",
                video_link     = 'video_link4',
                thumbnail      = 'thumbnail4',
                budget         = 40000000,
                price_per_view = 400,
                ad_category    = ad_cate4,
                like_count     = 400,
                quiz_count     = 400,
                )
        ad4.tag.add(ad_tag4)
        ad4.interests.add(interests4)
                
        ad_cate5 = AdvertisementCategory.objects.create(id=5, name='컴퓨터5')
        ad_tag5 = Tag.objects.create(id=5, name='개발5') 
        
        ad5 = Advertisement.objects.create(
                id             = 5,
                title          = "title5",
                advertiser     = advertiser, 
                description    = "description5",
                video_link     = 'video_link5',
                thumbnail      = 'thumbnail5',
                budget         = 50000000,
                price_per_view = 500,
                ad_category    = ad_cate5,
                like_count     = 500,
                quiz_count     = 500,
                )
        ad5.tag.add(ad_tag5)
        ad5.interests.add(interests5)
                
        ad_cate6 = AdvertisementCategory.objects.create(id=6, name='컴퓨터6')
        ad_tag6 = Tag.objects.create(id=6, name='개발6') 
        
        ad6 = Advertisement.objects.create(
                id             = 6,
                title          = "title6",
                advertiser     = advertiser, 
                description    = "description6",
                video_link     = 'video_link6',
                thumbnail      = 'thumbnail6',
                budget         = 60000000,
                price_per_view = 600,
                ad_category    = ad_cate6,
                like_count     = 600,
                quiz_count     = 600,
                switch = True,
                )
        ad6.tag.add(ad_tag6)
        ad6.interests.add(interests6)
                    
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
                    "advertisement_id":7
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

        response = c.get("/user/advertisements?offset=0&limit=1",
                **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {"RESULT": [{
                    'advertisement_id':  1,
                    'title':             'title1',
                    'thumbnail':         'thumbnail1',
                    'price_per_view':    100,
                }],
                "total_count":2 
                } 
        ) 

        response = c.post("/user/advertisements?offset=0&limit=1&tag=개발3",
                 **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {"RESULT": [{
                    'advertisement_id':  3,
                    'title':             'title3',
                    'thumbnail':         'thumbnail3',
                    'price_per_view':    300,
                }],
                "total_count":1
                } 
        ) 

        response = c.post("/user/advertisements?offset=0&limit=1&category_id=6",
                **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {"RESULT": [{
                    'advertisement_id':  6,
                    'title':             'title6',
                    'thumbnail':         'thumbnail6',
                    'price_per_view':    600,
                }],
                "total_count":1 
                } 
        ) 
        
        test1 = {
                "order_by": [
                    {"field":"price_per_view","asc":True}
                    ]
                }
        response = c.post("/user/advertisements?offset=0&limit=1", json.dumps(test1),
                **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {"RESULT": [{
                    'advertisement_id':  1,
                    'title':             'title1',
                    'thumbnail':         'thumbnail1',
                    'price_per_view':    100,
                }],
                "total_count":3 
                } 
        ) 
 
        test2 = {
                "order_by":[
                    {"field":"like_count","asc":False}
                    ]
                }
        response = c.post("/user/advertisements?offset=0&limit=1", json.dumps(test2),
                **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {"RESULT": [{
                    'advertisement_id':  6,
                    'title':             'title6',
                    'thumbnail':         'thumbnail6',
                    'price_per_view':    600,
                }],
                "total_count":3 
                } 
        )

        response = c.get("/user/advertisements?offset=0&limit=1",
                **{"HTTP_Authorization": Authorization_user,"content_type":"application/json"}
                    ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {"RESULT": [{
                    'advertisement_id':  1,
                    'title':             'title1',
                    'thumbnail':         'thumbnail1',
                    'price_per_view':    100,
                }],
                "total_count":2 
                } 
        ) 
        
        response = c.get("/advertiser/advertisements",
                **{"HTTP_Authorization": Authorization_advertiser,"content_type":"application/json"}
                    ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {"on_advertisement": [
                    {
                    'advertisement_id':  1,
                    'title':             'title1',
                    'thumbnail':         'thumbnail1',
                    },
                    {
                    'advertisement_id':  3,
                    'title':             'title3',
                    'thumbnail':         'thumbnail3',
                    },
                    {
                    'advertisement_id':  6,
                    'title':             'title6',
                    'thumbnail':         'thumbnail6',
                    },
                ],
                "off_advertisement": [ 
                    {
                    'advertisement_id':  4,
                    'title':             'title4',
                    'thumbnail':         'thumbnail4',
                    },
                    {
                    'advertisement_id':  5,
                    'title':             'title5',
                    'thumbnail':         'thumbnail5',
                    }
                ]
                }
        ) 
