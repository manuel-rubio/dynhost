# -*- coding: utf-8 -*-
from registration.forms import RegistrationFormUniqueEmail, RegistrationFormTermsOfService
from django.contrib.auth.forms import PasswordResetForm
from captcha.fields import ReCaptchaField

class RecaptchaRegistrationForm(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):
    captcha = ReCaptchaField()

class RecaptchaPasswordResetForm(PasswordResetForm):
	captcha = ReCaptchaField()
