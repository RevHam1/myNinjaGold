from django.urls import path
from myninja_gold_app.views import index

from . import views

urlpatterns = [
    # path('', index),
    path('', views.index, name='index'),
]
