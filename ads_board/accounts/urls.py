from django.urls import path
from . import views
from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('profile/', views.profile, name='profile'),
]
