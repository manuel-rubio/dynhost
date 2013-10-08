# -*- coding: utf-8 -*-
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.forms import PasswordResetForm
from captcha.fields import ReCaptchaField

class RecaptchaRegistrationForm(RegistrationFormUniqueEmail):
    captcha = ReCaptchaField()

class RecaptchaPasswordResetForm(PasswordResetForm):
	captcha = ReCaptchaField()
