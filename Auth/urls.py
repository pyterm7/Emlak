from django.urls import path 

from Auth.views import (
    SignIn, 
    SignUp, 
    SignOut, 
    MyAccount, 
    SetSocialAccount, 
    ChangeAvatar, 
    EditAccount, 
    GetPassport, 
    AddUser2AgencyTeam, 
    SeeUser, 
    ChangeVOEN,
)

urlpatterns = [
    path('sign-in/', SignIn, name='sign-in-page'),
    path('sign-up/', SignUp, name='sign-up-page'),
    path('sign-out/', SignOut, name='sign-out-page'),
    path('my-account/', MyAccount, name='my-account'),
    path('set-social-account/', SetSocialAccount, name="set-social-account"),
    path('change-avatar/', ChangeAvatar, name="change-avatar"),
    path('edit-account/', EditAccount, name="edit-account"),
    path('level-up/', GetPassport, name="get-passport"),
    path('add-user-2-agency-team/', AddUser2AgencyTeam, name="add-user-2-agency-team"),
    path('user/', SeeUser, name="see-user"),
    path('change-voen/', ChangeVOEN, name="change-voen"),
]