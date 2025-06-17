from django.urls import path

from word import views

app_name = 'word'

urlpatterns = [
    path('list/', views.WordListView.as_view(), name='list'),
    path('reverse/', views.WordListView.as_view(), name='reverse'),
    path('create/', views.WordCreateView.as_view(), name='create'),
]
