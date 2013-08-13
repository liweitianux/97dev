
AUTHENTICATION_BACKENDS = (
    'profile.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)