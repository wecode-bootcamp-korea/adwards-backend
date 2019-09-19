from django.db import models
from decimal import Decimal

class State(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'state'

class Gender(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'gender'

class InterestsType(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'interests_type'

class Bank(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=30) 
    
    class Meta:
        db_table = 'bank'

class IndustryType(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'industry_type'

class Advertiser(models.Model):
    email                   = models.EmailField(max_length = 254, unique = True)
    password                = models.CharField(max_length = 250)
    company_name            = models.CharField(max_length = 100)
    balance                 = models.DecimalField(max_digits = 14, decimal_places = 4, default = Decimal('0.0000'))
    business_license_number = models.CharField(max_length = 50)
    industry_type           = models.ForeignKey(IndustryType, on_delete = models.SET_NULL, null = True)
    contact                 = models.CharField(max_length = 50)
    company_address         = models.CharField(max_length = 100)
    company_description     = models.CharField(max_length = 2500, null = True)
    homepage                = models.URLField(max_length = 2500, null = True)
    thumbnail               = models.URLField(max_length = 2500, null = True)
    created_at              = models.DateTimeField(auto_now_add = True)
    updated_at              = models.DateTimeField(auto_now = True)
    deleted                 = models.BooleanField(default = False, null = True)

    class Meta:
        db_table = 'advertiser'

class User(models.Model):
    nickname       = models.CharField(max_length = 30, unique = True)
    email          = models.EmailField(max_length = 254, unique = True, null = True)
    password       = models.CharField(max_length = 250, null = True)
    user_name      = models.CharField(max_length = 254, null = True)
    age            = models.SmallIntegerField(null = True)
    state          = models.ForeignKey(State, on_delete = models.SET_NULL, null = True)
    gender         = models.ForeignKey(Gender, on_delete = models.SET_NULL, null = True)
    cellphone      = models.CharField(max_length = 20, null = True)
    thumbnail      = models.URLField(max_length = 2500, null = True)
    interests      = models.ManyToManyField(InterestsType)
    bank           = models.ForeignKey(Bank, on_delete = models.SET_NULL, null = True)
    account_owner  = models.CharField(max_length = 100)
    account_number = models.CharField(max_length = 100)
    created_at     = models.DateTimeField(auto_now_add = True)
    updated_at     = models.DateTimeField(auto_now = True)
    deleted        = models.BooleanField(default = False, null = True)
    
    class Meta:
        db_table = 'user'

class SocialAuth(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'social_auth'

class SocialAuthUser(models.Model):
    social_login_id = models.CharField(max_length=500)
    social_auth     = models.ForeignKey(SocialAuth, on_delete=models.SET_NULL, null=True)
    user            = models.ForeignKey(User, on_delete=models.PROTECT)
    nickname        = models.CharField(max_length=500, null=True)
    
    class Meta:
        db_table = 'social_auth_user'

