'''Defines URL patterns for blogs'''

from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    # Main page
    path(' ', views.index, name='index'),
    # Showing all topics page
    path('topics/', views.topics, name='topics'),
    # Showing a single topic.
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # Page for a new blog
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page for a new post
    path('new_entry/<int:topic_id>/' ,views.new_entry, name='new_entry'),
    # Page for edit the post
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry')
     ]