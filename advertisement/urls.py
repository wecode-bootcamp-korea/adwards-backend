from django.urls import path, include
from .views      import (
    AdvertisementView, 
    AdvertiserAdvertisementsView,
    UserAdvertisementsView, 
)

urlpatterns = [
    path('advertisement', AdvertisementView.as_view()),
    path('user/advertisements', UserAdvertisementsView.as_view()),
    path('advertiser/advertisements', AdvertiserAdvertisementsView.as_view()),
]
