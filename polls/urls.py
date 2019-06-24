from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('list/', views.poll_view, name='poll_view'),
    path('add/', views.add_poll, name='add'),
    path('edit/<int:poll_id>', views.edit_poll, name='edit_poll'),
    path('edit/<int:poll_id>/add/choice' , views.add_choice, name='add_choice'),
    path('edit/choice/<int:choice_id>', views.edit_choice, name='edit_choice'),
    path('delete/choice/<int:choice_id>', views.choice_delete, name='choice_delete'),
    path('delete/poll/<int:poll_id>/', views.poll_delete, name='poll_delete'),
    # polls/details/1
    # <int:poll_id> is to get the id of the poll, and poll_id typed here first
    # <int> is not requierd , it's optionally, but better to put if looking for intgers only
    # to know more about <int> search for python Path converters
    path('details/<int:poll_id>', views.poll_detailes, name='poll_details'),
    path('details/<int:poll_id>/vote', views.poll_vote, name='vote')
]
