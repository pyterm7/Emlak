from django.urls import path 

from Auth.views import SignIn, SignUp, SignOut, MyAccount, SetSocialAccount, ChangeAvatar

urlpatterns = [
    path('sign-in/', SignIn, name='sign-in-page'),
    path('sign-up/', SignUp, name='sign-up-page'),
    path('sign-out/', SignOut, name='sign-out-page'),
    path('my-account/', MyAccount, name='my-account'),
    path('set-social-account/', SetSocialAccount, name="set-social-account"),
    path('change-avatar/', ChangeAvatar, name="change-avatar"),
]