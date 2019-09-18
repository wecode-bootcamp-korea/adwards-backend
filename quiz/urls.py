from django.urls import path, include
from .views import QuizCreateView

urlpatterns = [
    path('quiz', QuizCreateView.as_view()),
]
