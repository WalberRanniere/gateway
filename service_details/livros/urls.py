from django.urls import path
from .views import LivroView

urlpatterns = [
    path("livros/<str:isbn>", LivroView.as_view()),
]
