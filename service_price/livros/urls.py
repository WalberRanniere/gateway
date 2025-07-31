from django.urls import path
from .views import PrecoView

urlpatterns = [
    path("precos/<str:isbn>", PrecoView.as_view()),
]
