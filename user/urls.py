from django.urls import path, include
from .views import UserSignup, AdvertiserSignup

urlpatterns = [
    path('signup/user', UserSignup.as_view()),
    path('signup/advertiser', AdvertiserSignup.as_view()),
]
