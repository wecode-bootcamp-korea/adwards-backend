from django.urls import path, include
from .views import QuizView

urlpatterns = [
    path('quiz', QuizView.as_view()),
]
