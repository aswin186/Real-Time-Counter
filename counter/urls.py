from django.urls import path
from .views import increment_counter, counter_view, decrement_counter

urlpatterns = [
    path('', counter_view, name='counter_view'),
    path('increment/', increment_counter, name='increment_counter'),
    path('decrement/', decrement_counter, name='increment_counter'),
]
