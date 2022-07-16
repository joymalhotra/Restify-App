from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from accounts.views import RegistrationAPIView, UserAPIView, EditProfileAPIView, RetrieveAvatarAPIView

app_name = 'accounts'
urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('profile/', UserAPIView.as_view(), name='profile'),
    path('editProfile/', EditProfileAPIView.as_view(), name="edit profile"),
    path('pictures/<str:avatar_url>', RetrieveAvatarAPIView.as_view(), name="avatar" ),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
