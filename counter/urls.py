from django.urls import path
from .views import increment_counter, counter_view

urlpatterns = [
    path('', counter_view, name='counter_view'),
    path('increment/', increment_counter, name='increment_counter'),
]
