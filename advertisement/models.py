from django.db import models
from user.models import *

class AdvertisementCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'ad_category'

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'tag'

class AdvertisementTag(models.Model):
    advertisement = models.ForeignKey('Advertisement', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ad_tag'

class Advertisement(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    advertiser = models.ForeignKey(Advertiser, on_delete=models.PROTECT)
    interests = models.ManyToManyField(InterestsType, through='AdvertisementsInterests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, null=True)
    ad_category = models.ForeignKey(AdvertisementCategory, on_delete=models.SET_NULL, null=True)
    video_link = models.URLField(max_length=2500)
    budget = models.DecimalField(max_digits=20, decimal_places=4)
    price_per_view = models.DecimalField(max_digits=15, decimal_places=4)
    switch = models.BooleanField(default=False, null=True)
    tag = models.ManyToManyField(Tag, through=AdvertisementTag)
    thumbnail = models.URLField(max_length=2500, null=True)
    quiz_history = models.ManyToManyField(User, through='QuizHistory') 
    view_count = models.IntegerField(default=0, null=True) 
    like_count = models.IntegerField(default=0, null=True) 
    quiz_count = models.IntegerField(default=0, null=True)

    class Meta:
        db_table = 'advertisement'

class AdvertisementLike(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ad_like'

class QuizHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz_history'

class RewardHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    quiz_history = models.ForeignKey(QuizHistory, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reward_history'

class AdvertisementsInterests(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    interests_type = models.ForeignKey(InterestsType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ad_interests' 
