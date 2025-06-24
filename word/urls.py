from django.urls import path

from word import views

app_name = 'word'

urlpatterns = [
    path('list/', views.WordListView.as_view(), name='list'),
    path('list/reverse/', views.WordListView.as_view(), name='reverse'),
    path('pairs/', views.WordPairListView.as_view(), name='pairs'),
    path('pairs/reverse/', views.WordPairListView.as_view(), name='pairs_reverse'),
    path('create/', views.WordCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.WordUpdateView.as_view(), name='update'),
    path('ignore/<int:pk>/', views.ignore_word, name='ignore'),
]
