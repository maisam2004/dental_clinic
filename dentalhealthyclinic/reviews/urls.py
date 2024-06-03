from django.urls import path
from . import views

urlpatterns = [
    path('add_review/', views.add_review, name='add_review'),
    path('', views.display_reviews, name='reviews'),
    #path('order_history/<order_number>/',views.order_history,name="order_history"),
]