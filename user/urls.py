from .views import UserSignup, AdvertiserSignup, UserSignin, AdvertiserSignin

from django.urls import path, include

urlpatterns = [
    path('signup/user', UserSignup.as_view()),
    path('signup/advertiser', AdvertiserSignup.as_view()),
    path('signin/user', UserSignin.as_view()),
    path('signin/advertiser', AdvertiserSignin.as_view())
]
