| Title                | UserSignup                                                   |
| -------------------- | ------------------------------------------------------------ |
| Method               | POST                                                         |
| URL                  | /signup/user                                                 |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params          | { user_name: [string], nickname: [string](unique), email: [string](unique), password: [string], age: [integer], state_id: [integer], gender_id: [integer], cellphone: [string],   thumbnail: [string], bank_id: [integer], account_owner: [string], account_number: [string], interests: [array composed of integer] } |
| Success Response     | Code:200, Content: None                                      |
| Error Response       | Code: 400,Conetent: "ERROR": "INVALID_EMAIL" Code: 400,Conetent: "ERROR": "EMAIL_EXISTING" Code: 400,Conetent: "ERROR": "NICKNAME_EXISTING" Code: 400,Conetent: "ERROR": "INVALID_PASSWORD" Code: 400,Conetent: "ERROR": "NAME_MISSING" Code: 400,Conetent: "ERROR": "KEY_MISSING" |
| Sample Call          | { user_name: "한바름", nickname: "별명", email: "mail@mail.com", password: "12345678", age: 30, state_id: 1, gender_id: 1, cellphone: 01012341234, thumbnail: "http://someimagelink.com/imgae", bank_id: 1, account_owner: "한바름", account_number: "010010010", interests: [1, 2, 3, 4] } |
| Notes                | Ref. banks, genders, interests_types   -Validation fail condition  name: 0 character  email: not email form, duplicated value nickname: duplicated value password: none or under 8 character |


| Title                | AdvertiserSignup                                             |
| -------------------- | ------------------------------------------------------------ |
| Method               | POST                                                         |
| URL                  | /signup/advertiser                                           |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params          | { company_name: [string](unique), business_license_number: [integer], email: [string](unique), password: [string], industry_type_id: [integer], contact: [string], thumbnail: [string], homepage: [string], company_address: [string], company_description: [string], } |
| Success Response     | Code:200, Content: None                                      |
| Error Response       | Code: 400,Conetent: "ERROR": "INVALID_EMAIL" Code: 400,Conetent: "ERROR": "EMAIL_EXISTING" Code: 400,Conetent: "ERROR": "INVALID_PASSWORD" Code: 400,Conetent: "ERROR": "COMPANYNAME_MISSING" Code: 400,Conetent: "ERROR": "KEY_MISSING" |
| Sample Call          | { company_name: "위코드", business_license_number: "12341234", email: "mail@mail.com", password: "12345678", industry_type_id: 1, contact: "01012341234", thumbnail:"http://someimagelink.com/imgae", homepage:"wecode.co.kr", company_address: "서울 강남구 위워크 7층", company_description: "한국 최고의 개발자 양성 학교", } |
| Notes                | Ref. industry_types    -Validation fail condition  company_name: 0 character  email: not email form, duplicated value password: none or under 8 character |

| Title                | AdvertiserSignin                                             |
| -------------------- | ------------------------------------------------------------ |
| Method               | POST                                                         |
| URL                  | /signin/advertiser                                           |
| URL Params           | None                                                         |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params          | { "email":"wecode@mail.net", "password":"12341234" }         |
| Success Response     | Code:200, Content: {"access_token":"dlasdlkajsdklasjdlsdk;asld;asdka;dkas;dla;sdklaa;sdk;akd;"} |
| Error Response       | "Code: 400,Conetent: ""ERROR"": ""MISSING_DATA"" 아이디 오기입 - ""ERROR"":""ID_NOT_EXIST"" 비밀번호 오기입 - ""ERROR"":""INVALID_PWD""" |
| access_token content | { "user_id":"wecode@mail.net", "user_type":"advertiser", "exp":"312893014", "iat":"123124213" } |
| Notes                |                                                              |

| Title                | UserSignin                                                   |
| -------------------- | ------------------------------------------------------------ |
| Method               | POST                                                         |
| URL                  | /signin/user                                                 |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params          | { "email":"wecode@mail.net", "password":"12341234" }         |
| Success Response     | Code:200, Content: {"access_token":"dlasdlkajsdklasjdlsdk;asld;asdka;dkas;dla;sdklaa;sdk;akd;"} |
| Error Response       | Code: 400,Conetent: "ERROR": "MISSING_DATA" 아이디 오기입 - "ERROR":"ID_NOT_EXIST" 비밀번호 오기입 - "ERROR":"INVALID_PWD" |
| access_toke content  | { "user_id":"wecode@mail.net", "user_type":"user", "exp":"312893014", "iat":"123124213" } |
| Notes                |                                                              |

| Title                                                        | Advertisement_Create                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Method                                                       | POST                                                         |
| URL                                                          | /advertisement                                               |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params                                                  | {  title: [string], description: [string], ad_category_id: [integer], video_link: [string], thumbnail: [string], budget: [integer] price_per_view: [integer], tag: [srting_array], interests_type_id: [Integer_array] } |
| Success Response                                             | Code: 200, Content: "advertisement_id" : advertisement_id    |
| Error Response                                               | Code: 400, Content: "ERROR":"KEY_MISSING"  Code: 401, Content: "ERROR":"INVALID_USER" Code: 401, Content: "ERROR":"INVALID_TOKEN" Code: 401, Content: "ERROR":"ID_NOT_EXIST" Code: 401, Content: "ERROR":"ERROR":"LOGIN_REQUIERD" |
| Sample Call                                                  | { title: "위코드광고1", description: "코드를 사랑하는 사람들 오세요!", ad_category_id: 1, video_link: "http://wecode.com", thumbnail: "http://wecode.com/img"  price_per_view: 1000, tag: ['코드','컴퓨터','개발','웹'], interests_type_id: [1,3,5,7,9] } |
| Notes                                                        | * Advertiser Login Required Ref. ad_categories               |

| Title                                                        | Advertisements_on/off_for_Advertiser                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Method                                                       | GET                                                          |
| URL                                                          | /advertiser/advertisements                                   |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params                                                  | None                                                         |
| Success Response                                             | Code: 200, Content:  { on_advertisement:[ { advertisement_id: [integer], thumbnail: [string], title: [string]  } ], off_advertisement:[ { advertisement_id: [integer], thumbnail: [string], title: [string] } ] } |
| Error Response                                               | Code: 400, Content: "ERROR":"LOGIN_REQUIRED"                 |
| Sample Call                                                  | /advertiser/advertisements                                   |
| Notes                                                        | *Advertiser login required                                   |


| Title                                                        | Advertisements_Sorted_by_user_interests_for_User             |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Method                                                       | GET                                                          |
| URL                                                          | /user/advertisements                                         |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | offset= [integer](default=0),  limit= [integer](default=3)   |
| Data Params                                                  | None                                                         |
| Success Response                                             | Code: 200, Content:  { "RESULT": [ ... { advertisement_id: [integer], title: [string], thumbnail: [string], price_per_view: [integer], created_at: [string] } ], "TOTAL": [integer]  } |
| Error Response                                               | Code: 400, Content: "ERROR":"KEY_MISSING"  Code: 400, Content: "ERROR":"INVALID_QUERYSTRING" Code: 400, Content: "ERROR":"LOGIN_REQUIRED" |
| Sample Call                                                  | /advertisement?offset=10&limit=14&price_per_view=set  or /advertisement?offset=10&limit=14&category_id=3 or /advertisement?offset=05&limit=10&advertiser=set |
| Notes                                                        | *User Login Required                                         |

| Title                                                        | Advertisements_Sorted_by_Field                               |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Method                                                       | GET                                                          |
| URL                                                          | /advertiser/advertisements                                   |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           |  offset= [integer](default=0),  limit= [integer](default=3),  category_id= [integer](Ref. ad_categories),  tag = [string]   |
| Data Params                                                  | { order_by:  [  ... { field: [string], asc: [boolean] }  ...  ]  } |
| Success Response                                             | Code: 200, Content:  { "RESULT": [ ... { advertisement_id: [integer], title: [string], thumbnail: [string], price_per_view: [integer], } ], "TOTAL": [integer]  } |
| Error Response                                               | Code: 400, Content: "ERROR":"KEY_MISSING"  Code: 400, Content: "ERROR":"INVALID_QUERYSTRING" Code: 400, Content: "ERROR":"LOGIN_REQUIRED" |
| Sample Call                                                  | /advertisement?offset=10&limit=14&tag=자동차  request : { order_by:  [   { field: "price_per_view" , asc: true }, { field: "like_count", asc: false }   ]  }  * 자동차 태그가 달린 광고물을, price_per_view 오름차순, like_count 내림차순으로 정렬해서 10번째에서 13번째 광고까지 데이터 전달한다. |
| Notes                                                        | field value:  price_per_view: 금액  like_count: 좋아요  view_count: 조회수   category_id = 카테고리별 조회, tag: 태그입력하면 태그 걸린 게시물 조회합니다.    query 스트링, 바디 아무 값 없으면 제일 먼저 만들어진 광고부터 순서대로 리스팅 됨 |

| Title                                                        | Advertisement_Detail_for_User                                |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Method                                                       | GET                                                          |
| URL                                                          | /user/advertisement/<advertisement_id>                       |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params                                                  | None                                                         |
| Success Response                                             | Code: 200, Content:   RESULT :  {  title: [string], description: [string], video_link: [string], price_per_view: [integer],  advertiser_id: [integer] company_name: [integer] tag: [array],   thumbnail: [string],  } |
| Error Response                                               | Code: 400, "ERROR":"INVALID_ADVERTISMENT_ID"  Code: 400, "ERROR":"UNAUTHNTICATED_ACCESS" |
| Sample Call                                                  | None                                                         |
| Notes                                                        | None                                                         |


| Title                                                        | Advertisement_Detail_for_Advertiser                          |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Method                                                       | GET                                                          |
| URL                                                          | /advertiser/advertisement/<advertisement_id>                 |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params                                                  | None                                                         |
| Success Response                                             | Code: 200, Content:   **Advertiser Logined** RESULT :  {  title: [string], description: [string], video_link: [string], view_count: [integer], price_per_view: [integer],  advertiser_id: [integer] tag: [array],   thumbnail: [string], budget: [integer], interests_type_id: [array], switch: [Boolean] } |
| Error Response                                               | Code: 400, "ERROR":"INVALID_ADVERTISMENT_ID"  Code: 400, "ERROR":"UNAUTHNTICATED_ACCESS" |
| Sample Call                                                  | None                                                         |
| Notes                                                        | *Advertiser Login Required                                   |

| Title                                                        | Advertisement_Update                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Method                                                       | POST                                                         |
| URL                                                          | /advertiser/advertisement/<advertisement_id>                 |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params                                                  | { title: [string], description: [string], ad_category_id: [integer_array],  video_link: [string], thumbnail: [string], tag: [string_array], swtich: [Boolean] } |
| Success Response                                             | Code: 200                                                    |
| Error Response                                               | Code: 400, "ERROR":"KEY_MISSING"  Code: 400, :ERROR":"INVALID_ADVERTISEMENT_ID" Code: 400, :ERROR":"INVALID_DATA_TYPE" Code: 400, :ERROR":"INVALID_INPUT" |
| Sample Call                                                  | { title: "위코드광고22", description: "개발자를 사랑하는 사람들 오세요!", ad_category_id: 1, video_link: "http://wecode.com", thumbnail: "http://wecode.com/img", price_per_view: 1000, tag: ['코드','컴퓨터','개발','웹'] } |
| Notes                                                        | *광고의 뷰당 가격은 절대 수정이 불가능합니다.                |


| Title                                                        | Advertisement_Delete                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Method                                                       | DELETE                                                       |
| URL                                                          | /advertiser/advertisement/<advertisement_id>                 |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params                                                  | None                                                         |
| Success Response                                             | Code: 200                                                    |
| Error Response                                               | Code: 400, "ERROR":"INVALID_ADVERTISEMENT_ID"                |
| Sample Call                                                  | None                                                         |
| Notes                                                        | Soft delete 실제 DB 에서 지워지는 것은 아님, 다만 지우면 광고주와 유저 모두에게 노출이 되지 않음! |

| Title            | quiz_create                                                  |
| ---------------- | ------------------------------------------------------------ |
| Method           | POST                                                         |
| URL              | 10.58.2.94:8000/quiz                                         |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params      | quiz_data = { "ad_id":1, "quizzes":[ { "title":"wecode quiz", "content":"what is wecode?", "choices":["교육기관", "부트캠프", "헌혈기관", "외주업체"], "answers":["교육기관", "부트캠프"] } ] |
| Success Response | Http response 200                                            |
| Error Response   | {"ERROR":"MISSING_DATA"}, status_code = 400 - data가 누락 될 시 |
| Sample Call      |                                                              |
| Notes            | 현재 광고 아이디와 퀴즈콘텐츠를 주시되, 퀴즈를 추가적으로 생성할 시 퀴즈별로 데이터를 리스트로 묶어서 위와 같이 주시면 됩니다. 해당 키값은 위와 동일합니다. |

| Title            | quiz_list                                                    |
|------------------|--------------------------------------------------------------|
| Method           | GET                                                          |
| URL              | /advertisement/<int:ad_id>/quiz                              |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params      | None                                                         |
| Success Response | [ { 'answer_type': 'multi_answer', 'choices': [ {'content': 'o', 'id': 1}, {'content': 'x', 'id': 2} ], 'content': '현재 교육중인 기수는 3기다.', 'created_at': '2019-09-25T13:39:10.925', 'question': '위코드', 'question_type': 'multi_choices' }, { 'answer_type': 'multi_answer', 'choices': [ {'content': '12', 'id': 3}, {'content': '15', 'id': 4}, {'content': '20', 'id': 5}, {'content': '21', 'id': 6} ], 'content': '현재 교육중인 기수는 몇명일까요?', 'created_at': '2019-09-25T13:39:10.943', 'question': '위코드', 'question_type': 'multi_choices' } ] |
| Error Response   | {"ERROR":"MISSING_DATA"}, status_code = 400 - data가 누락 될 시 |
| Sample Call      |                                                              |
| Notes            | 현재 광고 아이디와 퀴즈콘텐츠를 주시되, 퀴즈를 추가적으로 생성할 시 퀴즈별로 데이터를 리스트로 묶어서 위와 같이 주시면 됩니다. 해당 키값은 위와 동일합니다. |

| Title            | quiz_correct                                                 |
|------------------|--------------------------------------------------------------|
| Method           | POST                                                         |
| URL              | /quiz/answer                                                 |
| URL Params(Required)           | None                                                         |
| URL Params(Optional)           | None                                                           |
| Data Params      | test = { "ad_id":1, "user_answers": [ {"quiz_id": 1, "answers": [1]}, {"quiz_id": 2, "answers": [3,4,5]} ] } |
| Success Response | 모든 퀴즈 정답 일 경우 {"message":True} 하나라도 오답 일 경우 {"message":False} 200 |
| Error Response   | {"ERROR":"MISSING_DATA"}, status_code = 400 - data가 누락 될 시 |
| Sample Call      |                                                              |
| Notes            | 데이터 post 시, quiz_list api로 호출한 퀴즈와 선택지 데이터의 id갑을 일괄적으로  위와 같은 형태로 주시되 리스트에 담아서 주시면 됩니다. 광고 PK 또한 같이 주시면 됩니다. |

Normalization Table

gender

| id              | name         |
|-----------------|--------------|
| 1               | 남성          |
| 2               | 여성          |

interests_types

| id              | name         |
|-----------------|--------------|
| 1               | 쇼핑          |
| 2               | 의류          |
| 3               | 장난감         |
| 4               | 가구          |
| 5               | 레져활동       |
| 6               | 가족          |
| 7               | 결혼          |
| 8               | 데이트        |
| 9               | 육아          |
| 10              | 가전제품       |
| 11              | 컴퓨터         |
| 12              | 요가           |
| 13              | 주방           |
| 14              | 인테리어       |
| 15              | 샐러드         |
| 16              | 게임           |
| 17              | 독서           |
| 18              | 영화           |
| 19              | 음악           |
| 20              | 소셜네트워크   | 

reigon

| id              |name          |
|-----------------|--------------|
| 1               | 서울특별시     |
| 2               | 인천광역시     |
| 3               | 대전광역시     |
| 4               | 대구광역시     |
| 5               | 부산광역시     |
| 6               | 경기도         |
| 7               | 강원도         |
| 8               | 전라남도       |
| 9               | 전라북도       |
| 10              | 제주특별자치도 |
| 11              | 경상남도       |
| 12              | 경상북도       |
| 13              | 충청남도       |
| 14              | 충청북도       |

IndustryType

| id              | name           |
|-----------------|--------------|
| 1               | 제조업         |
| 2               | 금융           |
| 3               | 건설           |
| 4               | 건축           |
| 5               | 경영           |
| 6               | 부동산         |
| 7               | 보험           |
| 8               | 온라인판매     |
| 9               | 오프라인유통   |
| 10              | 헬스케어       |
| 11              | 항공           |
| 12              | 운송           |
| 13              | 온라인뱅킹     |
| 14              | 자동차         |
| 15              | 판매           |
| 16              | 엔터테인먼트   |
| 17              | 식음료산업     |
| 18              | 기타           |


ad_categories

| id              | name           |
|-----------------|--------------|
| 1               | 드라마         |
| 2               | 코믹           |
| 3               | 음악           |
| 4               | 동물           |
| 5               | 연예인         |
| 6               | 가족           |
| 7               | 해외           |
| 8               | 패러디         |
| 9               | 정보           |
| 10              | 영화           |

banks

| id    | name         | contact    |
|-------|------------|------------|
| 1     | KEB하나은행  | 02-1201-2001 |
| 2     | SC제일은행   | 02-1201-2002 |
| 3     | 국민은행     | 02-1201-2003 |
| 4     | 신한은행     | 02-1201-2004 |
| 5     | 외환은행     | 02-1201-2005 |
| 6     | 우리은행     | 02-1201-2006 |
| 7     | 한국시티은행 | 02-1201-2007 |
| 8     | 경남은행     | 02-1201-2008 |
| 9     | 광주은행     | 02-1201-2009 |
| 10    | 대구은행     | 02-1201-2010 |
| 11    | 부산은행     | 02-1201-2011 |
| 12    | 전북은행     | 02-1201-2012 |
| 13    | 제주은행     | 02-1201-2013 |
| 14    | 기업은행     | 02-1201-2014 |
| 15    | 농협         | 02-1201-2015 |
| 16    | 수협         | 02-1201-2016 |
