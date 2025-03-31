from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('process_money', views.process_money),
    path('reset', views.reset),
    path('ninja_gold/', views.ninja_gold_game, name='ninja_gold_game'),
    path('reset/', views.reset, name='reset'),
    path('get_gold_value/', views.get_gold_value, name='get_gold_value'),

    # path('supabasedata/', views.your_view, name='supabasedata'),
]
