from django.urls import path

from . import views

app_name = 'captcha'
urlpatterns = [
    path('generate/', views.GenerateCaptchaView.as_view(), name='generate'),
    path('validate/', views.ValidateCaptchaView.as_view(), name='validate')
]
