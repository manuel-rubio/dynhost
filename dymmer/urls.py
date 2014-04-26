# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from registration.backends.default.views import RegistrationView
from django.views.generic import TemplateView
from dymmer.forms import RecaptchaRegistrationForm, RecaptchaPasswordResetForm
from dymmer import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dymmer.views.home', name='home'),
    # url(r'^dymmer/', include('dymmer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^avisos-legales/condiciones-particulares-dominios', TemplateView.as_view(
        template_name='avisos-legales/condiciones-particulares-dominios.html'
    )),
    url(r'^avisos-legales/condiciones-generales-servicio', TemplateView.as_view(
        template_name='avisos-legales/condiciones-generales-servicio.html'
    )),
    url(r'^avisos-legales/privacidad', TemplateView.as_view(
        template_name='avisos-legales/privacidad.html'
    )),
    url(r'^avisos-legales', TemplateView.as_view(
        template_name='avisos-legales.html'
    )),
    url(r'^acerca-de', TemplateView.as_view(
        template_name='acerca-de.html'
    )),

    url(r'^user/register/complete', TemplateView.as_view(
        template_name='registration/registration_complete.html'
    )),
    url(r'^user/register/', RegistrationView.as_view(
        form_class=RecaptchaRegistrationForm
    )),
    url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset', {
        'password_reset_form': RecaptchaPasswordResetForm,
        'email_template_name': 'registration/password_reset_email.txt'
    }),
    url(r'^user/', include('registration.backends.default.urls')),

    url(r'^account/$', 'billing.views.index'),
    url(r'^purchase/domain/$', 'billing.views.purchase'),
    url(r'^payment/(?P<contract_id>\d+)/$', 'billing.views.payment'),
    url(r'^transfer/domain/$', 'billing.views.transfer'),
    url(r'^purchase/mail/plus/$', 'billing.views.mail_plus_purchase'),
    url(r'^purchase/mail/premium/$', 'billing.views.mail_premium_purchase'),
    url(r'^purchase/mail/redirect/$', 'billing.views.mail_redirect_purchase'),
    url(r'^purchase/db/mysql/$', 'billing.views.mysql_purchase'),
    url(r'^purchase/revoke/(?P<contract_id>\d+)/$', 'billing.views.revoke'),
    url(r'^deregister/$', 'billing.views.deregister'),
    url(r'^invoice/(?P<contract_id>\d+)/(?P<type>[a-z]+)/$', 'billing.views.invoice'),

    url(r'^dns/$', 'dns.views.domains.index'),
    url(r'^dns/(?P<page_id>\d+)/$', 'dns.views.domains.index'),
    url(r'^dns/(?P<dom_id>\d+)/edit/$', 'dns.views.domains.edit'),
    url(r'^dns/(?P<dom_id>\d+)/delete/$', 'dns.views.domains.delete'),
    url(r'^dns/new/$', 'dns.views.domains.new'),

    url(r'^ftp/$', 'ftp.views.index'),
    url(r'^ftp/(?P<page_id>\d+)/$', 'ftp.views.index'),
    url(r'^ftp/(?P<ftp_id>\d+)/edit/$', 'ftp.views.edit'),
    url(r'^ftp/(?P<ftp_id>\d+)/delete/$', 'ftp.views.delete'),
    url(r'^ftp/new/$', 'ftp.views.new'),

    url(r'^records/(?P<rec_id>\d+)/edit/$', 'dns.views.records.edit'),
    url(r'^records/(?P<rec_id>\d+)/delete/$', 'dns.views.records.delete'),
    url(r'^records/(?P<dom_id>\d+)/new/$', 'dns.views.records.new'),

    url(r'^mailbox/(?P<dom_id>\d+)/$', 'mail.views.mailboxes.index'),
    url(r'^mailbox/(?P<dom_id>\d+)/(?P<page_id>\d+)/$', 'mail.views.mailboxes.index'),
    url(r'^mailbox/(?P<mbox_id>\d+)/edit/$', 'mail.views.mailboxes.edit'),
    url(r'^mailbox/(?P<mbox_id>\d+)/delete/$', 'mail.views.mailboxes.delete'),
    url(r'^mailbox/(?P<dom_id>\d+)/new/$', 'mail.views.mailboxes.new'),

    url(r'^mail/redirect/(?P<dom_id>\d+)/$', 'mail.views.redirects.index'),
    url(r'^mail/redirect/(?P<dom_id>\d+)/(?P<page_id>\d+)/$', 'mail.views.redirects.index'),
    url(r'^mail/redirect/(?P<mbox_id>\d+)/edit/$', 'mail.views.redirects.edit'),
    url(r'^mail/redirect/(?P<mbox_id>\d+)/delete/$', 'mail.views.redirects.delete'),
    url(r'^mail/redirect/(?P<dom_id>\d+)/new/$', 'mail.views.redirects.new'),

    url(r'^database/$', 'database.views.databases.index'),
    url(r'^database/(?P<page_id>\d+)/$', 'database.views.databases.index'),
    url(r'^database/(?P<db_id>\d+)/show/$', 'database.views.databases.show'),
    url(r'^database/(?P<db_id>\d+)/delete/$', 'database.views.databases.delete'),
    url(r'^database/(?P<lk_id>\d+)/unlink/$', 'database.views.databases.unlink'),
    url(r'^database/(?P<db_id>\d+)/link/$', 'database.views.databases.link'),
    url(r'^database/new/$', 'database.views.databases.new'),

    url(r'^database/(?P<lk_id>\d+)/exec/$', 'database.views.databases.execute'),

    url(r'^database/user/$', 'database.views.users.index'),
    url(r'^database/user/(?P<page_id>\d+)/$', 'database.views.users.index'),
    url(r'^database/user/(?P<user_id>\d+)/edit/$', 'database.views.users.edit'),
    url(r'^database/user/(?P<user_id>\d+)/delete/$', 'database.views.users.delete'),
    url(r'^database/user/(?P<lk_id>\d+)/unlink/$', 'database.views.users.unlink'),
    url(r'^database/user/(?P<user_id>\d+)/link/$', 'database.views.users.link'),
    url(r'^database/user/new/$', 'database.views.users.new'),

    url(r'^dynamic/mail/redirect/(?P<rec_id>\d+)/$', 'mail.views.redirects_dynamic.index'),
    url(r'^dynamic/mail/redirect/(?P<rec_id>\d+)/(?P<page_id>\d+)/$', 'mail.views.redirects_dynamic.index'),
    url(r'^dynamic/mail/redirect/(?P<mbox_id>\d+)/edit/$', 'mail.views.redirects_dynamic.edit'),
    url(r'^dynamic/mail/redirect/(?P<mbox_id>\d+)/delete/$', 'mail.views.redirects_dynamic.delete'),
    url(r'^dynamic/mail/redirect/(?P<rec_id>\d+)/new/$', 'mail.views.redirects_dynamic.new'),

    url(r'^dynamic/web/redirect/(?P<rec_id>\d+)/$', 'web.views.redirects_dynamic.index'),
    url(r'^dynamic/web/redirect/(?P<rec_id>\d+)/(?P<page_id>\d+)/$', 'web.views.redirects_dynamic.index'),
    url(r'^dynamic/web/redirect/(?P<redir_id>\d+)/edit/$', 'web.views.redirects_dynamic.edit'),
    url(r'^dynamic/web/redirect/(?P<redir_id>\d+)/delete/$', 'web.views.redirects_dynamic.delete'),
    url(r'^dynamic/web/redirect/(?P<rec_id>\d+)/new/$', 'web.views.redirects_dynamic.new'),

    url(r'^web/redirect/(?P<dom_id>\d+)/$', 'web.views.redirects.index'),
    url(r'^web/redirect/(?P<dom_id>\d+)/(?P<page_id>\d+)/$', 'web.views.redirects.index'),
    url(r'^web/redirect/(?P<hosting_id>\d+)/edit/$', 'web.views.redirects.edit'),
    url(r'^web/redirect/(?P<hosting_id>\d+)/delete/$', 'web.views.redirects.delete'),
    url(r'^web/redirect/(?P<dom_id>\d+)/new/$', 'web.views.redirects.new'),

    url(r'^web/hosting/(?P<dom_id>\d+)/$', 'web.views.hostings.index'),
    url(r'^web/hosting/(?P<dom_id>\d+)/(?P<page_id>\d+)/$', 'web.views.hostings.index'),
    url(r'^web/hosting/(?P<hosting_id>\d+)/edit/$', 'web.views.hostings.edit'),
    url(r'^web/hosting/(?P<hosting_id>\d+)/delete/$', 'web.views.hostings.delete'),
    url(r'^web/hosting/(?P<dom_id>\d+)/new/$', 'web.views.hostings.new'),

    url(r'^dynamic/$', 'dynamic.views.domains.index'),
    url(r'^dynamic/(?P<page_id>\d+)/$', 'dynamic.views.domains.index'),
    url(r'^dynamic/(?P<dom_id>\d+)/edit/$', 'dynamic.views.domains.edit'),
    url(r'^dynamic/(?P<dom_id>\d+)/delete/$', 'dynamic.views.domains.delete'),
    url(r'^dynamic/new/$', 'dynamic.views.domains.new'),
    url(r'^dynamic/help/$', TemplateView.as_view(
        template_name='dynamic_help.html'
    )),

    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'index.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^404/$', 'django.views.defaults.page_not_found'),
        (r'^500/$', 'django.views.defaults.server_error'),
        (r'^media/', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT} ),
    )
