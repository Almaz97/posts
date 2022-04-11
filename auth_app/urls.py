from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SignUpView, LoginView, UserDataView

urlpatterns = [
    path('v1/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('v1/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/sign_up/', SignUpView.as_view(), name='auth_sign_up'),
    path('v1/users/<int:pk>/', UserDataView.as_view(), name='user_data'),
]
