from django.urls import path
from . import views


urlpatterns = [
    path('cards', views.Cards.as_view()),
    path('cards/<int:id>', views.CardDetail.as_view()),
    path('lists', views.Lists.as_view()),
]
