from django.urls import path, include
from .views      import (
    AdvertisementView, 
    AdvertiserAdvertisementsView,
    UserAdvertisementsView, 
    AdvertiserAdvertisementDetailView ,
    UserAdvertisementDetailView, 
)

urlpatterns = [
    path('advertisement', AdvertisementView.as_view()),
    path('user/advertisements', UserAdvertisementsView.as_view()),
    path('advertiser/advertisements', AdvertiserAdvertisementsView.as_view()),
    path('user/advertisementdetail/<int:advertisement_id>',
        UserAdvertisementDetailView.as_view()
    ),
    path('advertiser/advertisementdetail/<int:advertisement_id>',
        AdvertiserAdvertisementDetailView.as_view()
    ),
]
