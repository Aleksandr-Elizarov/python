"""Define the scheme URL for learning_logs."""
from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Page for editing entries.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # Page for adding a new entry.
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Page for adding a new topic.
    path('new_topic/', views.new_topic, name='new_topic'),
    # Home page.
    path('', views.index, name='index'),
    # A page with a list of all topics.
    path('topics/', views.topics, name='topics'),
    # A page with detailed information on a separate topic.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
]
