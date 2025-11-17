from django.urls import path
from custom_auth.views.auth_views import RegisterView, LoginView, LogoutView, ProfileView, ChangePasswordView, DeleteUserView
from custom_auth.views.mock_views import OrdersView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change_password/', ChangePasswordView.as_view()),
    path('profile/delete/', DeleteUserView.as_view()),
    path('mock/orders/', OrdersView.as_view(), name='orders'),
]
