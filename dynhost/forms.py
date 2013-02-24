# -*- coding: utf-8 -*-
from recaptcha.client import captcha
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from registration.backends.default import DefaultBackend
from registration.forms import RegistrationFormUniqueEmail

class ReCaptcha(forms.Widget):
    input_type = None # Subclasses must define this.

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        html = u"<script>var RecaptchaOptions = {theme : '%s'};</script>" % (
            final_attrs.get('theme', 'white'))
        html += captcha.displayhtml(settings.RECAPTCHA_PUBLIC)
        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        return {
            'recaptcha_challenge_field': data.get('recaptcha_challenge_field', None),
            'recaptcha_response_field': data.get('recaptcha_response_field', None),
        }

# hack: Inherit from FileField so a hack in Django passes us the
# initial value for our field, which should be set to the IP
class ReCaptchaField(forms.FileField):
    widget = ReCaptcha
    default_error_messages = {
        'invalid-site-public-key': u"Invalid public key",
        'invalid-site-private-key': u"Invalid private key",
        'invalid-request-cookie': u"Invalid cookie",
        'incorrect-captcha-sol': u"Invalid entry, please try again.",
        'verify-params-incorrect': u"The parameters to verify were incorrect, make sure you are passing all the required parameters.",
        'invalid-referrer': u"Invalid referrer domain",
        'recaptcha-not-reachable': u"Could not contact reCAPTCHA server",
    }

    def clean(self, data, initial):
        if initial is None or initial == '':
            raise Exception("ReCaptchaField requires the client's IP be set to the initial value")
        resp = captcha.submit(data.get("recaptcha_challenge_field", None),
                              data.get("recaptcha_response_field", None),
                              settings.RECAPTCHA_PRIVATE, initial)
        if not resp.is_valid:
            raise forms.ValidationError(self.default_error_messages.get(
                    resp.error_code, "Unknown error: %s" % (resp.error_code)))

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()

class RecaptchaRegistrationForm(RegistrationFormUniqueEmail):
    captcha = ReCaptchaField()

class RecaptchaRegistrationBackend(DefaultBackend):
    def get_form_class(self, request):
        return RecaptchaRegistrationForm

#--- workaround ---

from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from registration.backends import get_backend

def register(request, backend, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None):
    backend = get_backend(backend)
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            new_user = backend.register(request, **form.cleaned_data)
            if success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, new_user)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)
