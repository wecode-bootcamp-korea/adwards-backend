from django.urls import path, include

from .views import AdvertisementCreateListGetView

urlpatterns = [
    path('advertisement', AdvertisementCreateListGetView.as_view()),
#    path('advertisement/<int:advertisement_id>', AdvertisementView.as_view()),
#    path('advertisement/like/<int:advertisement_id>', AdvertisementLikeView.as_view()),
]
