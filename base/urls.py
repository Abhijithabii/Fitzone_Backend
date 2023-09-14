from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", UserRegisterationAPIView.as_view(), name="create-user"),
    path("verifyotp/", VerifyOTP.as_view(), name='verifyotp'),
    path('updateprofile/<int:id>/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('changepassword/<int:id>/', PasswordChangeView.as_view(), name='change_password')
  

]