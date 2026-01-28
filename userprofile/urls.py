from django.urls import path

from userprofile import views

app_name = 'userprofile'

urlpatterns = [
    path('update/', views.UserProfileUpdateView.as_view(), name='update'),
]
