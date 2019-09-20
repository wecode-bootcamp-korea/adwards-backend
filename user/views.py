import json
import bcrypt

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import User, Advertiser, InterestsType, State, Gender, Bank, IndustryType, UsersInterests

class UserSignup(View):
    def post(self, request):
        reqst = json.loads(request.body)

        try:
            validate_email(reqst["email"])
        except ValidationError:
            return JsonResponse({"ERROR":"INVALID_EMAIL"}, status=400)

        if User.objects.filter(email=reqst["email"]).exists():
            return JsonResponse({"ERROR":"EMAIL_EXISTING"}, status=400)

        if User.objects.filter(nickname=reqst["nickname"]).exists():
            return JsonResponse({"ERROR":"NICKNAME_EXISTING"})

        if "password" not in reqst or len(reqst["password"]) < 8:
            return JsonResponse({"ERROR":"INVALID_PASSWORD"}, status=400)

        if len(reqst["user_name"]) == 0:
            return JsonResponse({"ERROR":"NAME_MISSING"}, status=400)
        
        try:
            byted_pw = bytes(reqst["password"], "UTF-8")
            hashed_pw = bcrypt.hashpw(byted_pw, bcrypt.gensalt())
            user = User(
                    user_name = reqst["user_name"],
                    nickname = reqst["nickname"],
                    email = reqst["email"],
                    password =hashed_pw.decode("UTF-8"),
                    age = reqst["age"],
                    state_id = reqst["state_id"],
                    gender_id = reqst["gender_id"],
                    cellphone = reqst["cellphone"],
                    thumbnail = reqst["thumbnail"],
                    bank_id = reqst["bank_id"],
                    account_owner = reqst["account_owner"],
                    account_number = reqst["account_number"]
                    )
            user.save()

            interests = [
                    UsersInterests(
                        interests_type_id = interest_id,
                        user_id = user.id
                    ) 
                    for interest_id in reqst["interests"]
            ]
            UsersInterests.objects.bulk_create(interests)

            return HttpResponse(status=200)

        except KeyError:
            JsonResponse({"ERROR":"KEY_MISSING"}, status=400)

class AdvertiserSignup(View):
    def post(self, request):
        reqst = json.loads(request.body)

        try:
            validate_email(reqst["email"])
        except ValidationError:
            return JsonResponse({"ERROR":"INVALID_EMAIL"}, status=400)

        if Advertiser.objects.filter(email=reqst["email"]).exists():
            return JsonResponse({"ERROR":"EMAIL_EXISTING"}, status=400)

        if "password" not in reqst or len(reqst["password"]) < 8:
            return JsonResponse({"ERROR":"INVALID_PASSWORD"}, status=400)

        if len(reqst["company_name"]) == 0:
            return JsonResponse({"ERROR":"COMPANYNAME_MISSING"}, status=400)

        try:
            byted_pw = bytes(reqst["password"], "utf-8")
            hashed_pw = bcrypt.hashpw(byted_pw, bcrypt.gensalt())
            Advertiser.objects.create(
                    email = reqst["email"],
                    password = hashed_pw.decode("UTF-8"),
                    company_name = reqst["company_name"],
                    business_license_number = reqst["business_license_number"],
                    industry_type_id = reqst["industry_type_id"],
                    contact = reqst["contact"],
                    company_address = reqst["company_address"],
                    company_description = reqst["company_description"],
                    homepage = reqst["homepage"],
                    thumbnail = reqst["thumbnail"]
            )
            return HttpResponse(status=200)
        
        except KeyError:
            JsonResponse({"ERROR":"KEY_MISSING"}, status=400)
