# -*- coding: utf-8 -*-
from registration.forms import RegistrationFormUniqueEmail
from captcha.fields import ReCaptchaField

class RecaptchaRegistrationForm(RegistrationFormUniqueEmail):
    captcha = ReCaptchaField()
