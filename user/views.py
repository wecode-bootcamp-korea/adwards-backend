import jwt
import json
import bcrypt
from datetime import datetime, timedelta

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import User, Advertiser, InterestsType, State, Gender, Bank, IndustryType, UsersInterests
from adwards.settings import SECRET_KEY

class UserSignup(View):
    def post(self, request):
        request = json.loads(request.body)

        try:
            validate_email(request["email"])
        except ValidationError:
            return JsonResponse({"ERROR":"INVALID_EMAIL"}, status=400)

        if User.objects.filter(email=request["email"]).exists():
            return JsonResponse({"ERROR":"EMAIL_EXISTING"}, status=400)

        if User.objects.filter(nickname=request["nickname"]).exists():
            return JsonResponse({"ERROR":"NICKNAME_EXISTING"})

        if "password" not in request or len(request["password"]) < 8:
            return JsonResponse({"ERROR":"INVALID_PASSWORD"}, status=400)

        if len(request["user_name"]) == 0:
            return JsonResponse({"ERROR":"NAME_MISSING"}, status=400)
        
        try:
            byted_pw = bytes(request["password"], "UTF-8")
            hashed_pw = bcrypt.hashpw(byted_pw, bcrypt.gensalt())
            user = User(
                    user_name = request["user_name"],
                    nickname = request["nickname"],
                    email = request["email"],
                    password =hashed_pw.decode("UTF-8"),
                    age = request["age"],
                    state_id = request["state_id"],
                    gender_id = request["gender_id"],
                    cellphone = request["cellphone"],
                    thumbnail = request["thumbnail"],
                    bank_id = request["bank_id"],
                    account_owner = request["account_owner"],
                    account_number = request["account_number"]
                    )
            user.save()

            interests = [
                    UsersInterests(
                        interests_type_id = interest_id,
                        user_id = user.id
                    ) 
                    for interest_id in request["interests"]
            ]
            UsersInterests.objects.bulk_create(interests)

            return HttpResponse(status=200)

        except KeyError:
            JsonResponse({"ERROR":"KEY_MISSING"}, status=400)

class AdvertiserSignup(View):
    def post(self, request):
        request = json.loads(request.body)

        try:
            validate_email(request["email"])
        except ValidationError:
            return JsonResponse({"ERROR":"INVALID_EMAIL"}, status=400)

        if Advertiser.objects.filter(email=request["email"]).exists():
            return JsonResponse({"ERROR":"EMAIL_EXISTING"}, status=400)

        if "password" not in request or len(request["password"]) < 8:
            return JsonResponse({"ERROR":"INVALID_PASSWORD"}, status=400)

        if len(request["company_name"]) == 0:
            return JsonResponse({"ERROR":"COMPANYNAME_MISSING"}, status=400)

        try:
            byted_pw = bytes(request["password"], "utf-8")
            hashed_pw = bcrypt.hashpw(byted_pw, bcrypt.gensalt())
            Advertiser.objects.create(
                    email = request["email"],
                    password = hashed_pw.decode("UTF-8"),
                    company_name = request["company_name"],
                    business_license_number = request["business_license_number"],
                    industry_type_id = request["industry_type_id"],
                    contact = request["contact"],
                    company_address = request["company_address"],
                    company_description = request["company_description"],
                    homepage = request["homepage"],
                    thumbnail = request["thumbnail"]
            )
            return HttpResponse(status=200)
        
        except KeyError:
            JsonResponse({"ERROR":"KEY_MISSING"}, status=400)

class UserSignin(View):
    def post(self, request):
        try:
            reqst = json.loads(request.body)

            if User.objects.filter(email=reqst['email']).exists():
                user = User.objects.get(email=reqst['email'])
            else:
                return JsonResponse({"ERROR":"ID_NOT_EXIST"}, status=401)

            if bcrypt.checkpw(reqst['password'].encode('utf-8'), user.password.encode('utf-8')):
                payload = {
                        'user_id'   :user.email,
                        'user_type' :'user',
                        'exp'       :datetime.utcnow() + timedelta(days=1),
                        'iat'       :datetime.utcnow()
                        }
                token = jwt.encode(payload, SECRET_KEY, "HS256")

                return JsonResponse({"access_token":token.decode('utf-8')})
            else:
                return JsonResponse({"ERROR":"INVALID_PWD"}, status=401)
        except KeyError:
            return JsonResponse({"ERROR":"MISSING_DATA"}, status=400)

class AdvertiserSignin(View):
    def post(self, request):
        try:
            reqst = json.loads(request.body)

            if Advertiser.objects.filter(email=reqst['email']).exists():
                advertiser = Advertiser.objects.get(email=reqst['email'])
            else:
                return JsonResponse({"ERROR":"ID_NOT_EXIST"}, status=401)

            if bcrypt.checkpw(reqst['password'].encode('utf-8'), advertiser.password.encode('utf-8')):
                payload = {
                        'user_id'   :advertiser.email,
                        'user_type' :'advertiser',
                        'exp'       :datetime.utcnow() + timedelta(days=1),
                        'iat'       :datetime.utcnow()
                        }
                token = jwt.encode(payload, SECRET_KEY, "HS256")

                return JsonResponse({"access_token":token.decode('utf-8')})
            else:
                return JsonResponse({"ERROR":"INVALID_PWD"}, status=401)
        except KeyError:
            return JsonResponse({"ERROR":"MISSING_DATA"}, status=400)
