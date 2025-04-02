from django.urls import path
from . import views
from .views import MyTokenObtainPairView,GetUserView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', GetUserView.as_view(), name='get_user'),
    path("register/", views.registration_view ),

    path("verify/",views.verify_otp),
    path('password-reset/request/', views.password_reset_request, name='password-reset-request'),

    path('password-reset/confirm/', views.password_reset_confirm, name='password-reset-confirm'),



]