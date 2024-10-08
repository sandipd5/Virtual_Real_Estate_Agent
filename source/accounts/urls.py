from django.urls import path
from main.views import user_login
from .views import (
    LogInView, ResendActivationCodeView, RemindUsernameView, SignUpView, ActivateView, LogOutView,
    ChangeEmailView, ChangeEmailActivateView, ChangeProfileView, ChangePasswordView,
    RestorePasswordView, RestorePasswordDoneView, RestorePasswordConfirmView, LogOutConfirmView,
)

app_name = 'accounts'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/confirm/', LogOutConfirmView.as_view(), name='log_out_confirm'),
    path('log-out/', LogOutView.as_view(), name='log_out'),

    path('resend/activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),

    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate/<code>/', ActivateView.as_view(), name='activate'),

    path('restore/password/', RestorePasswordView.as_view(), name='restore_password'),
    path('restore/password/done/', RestorePasswordDoneView.as_view(), name='restore_password_done'),
    path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),

    path('remind/username/', RemindUsernameView.as_view(), name='remind_username'),

    path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('change/email/', ChangeEmailView.as_view(), name='change_email'),
    path('change/email/<code>/', ChangeEmailActivateView.as_view(), name='change_email_activation'),
    # path('main/', include('main.urls')), #chatbot changes if necessary will do it
    path('log-in/realtor/', user_login, {'user_type': 'realtor'}, name='realtor_login'),
    path('log-in/customer/', user_login, {'user_type': 'customer'}, name='customer_login'),
]
