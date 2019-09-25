from django.urls import path, include
from .views import QuizView, QuizCorrectView, QuizListView

urlpatterns = [
    path('quiz', QuizView.as_view()),
    path('quiz/answer', QuizCorrectView.as_view()),
    path('advertisement/<int:ad_id>/quiz', QuizListView.as_view())
]
