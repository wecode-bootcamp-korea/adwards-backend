from django.urls import path, include

urlpatterns = [
    path('', include('user.urls')),
    path('', include('quiz.urls')),
    path('', include('advertisement.urls')),
]
