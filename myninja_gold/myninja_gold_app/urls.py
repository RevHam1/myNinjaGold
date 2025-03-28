from django.urls import path
from myninja_gold_app.views import index

urlpatterns = [
    path('', index),
]
