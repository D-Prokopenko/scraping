
from django.urls import path
from .views import LoginView, LogoutView, RegisterView, PersonAreaView, DelPersonView, MsgAdminView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update/', PersonAreaView.as_view(), name='update'),
    path('delete/', DelPersonView.as_view(), name='delete'),
    path('contact/', MsgAdminView.as_view(), name='contact'),
]
