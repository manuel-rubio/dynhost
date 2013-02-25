# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from dynhost.forms import RecaptchaRegistrationForm
from dynhost import settings

urlpatterns = patterns('',
    # ver templateresponse y extra_context para agregar funcionalidad
    # a estas vistas.
    url(r'^user/register/complete', direct_to_template, {
        'template': 'registration/registration_complete.html'
    }),
    url(r'^user/register/', 'dynhost.forms.register', {
        'backend': 'dynhost.forms.RecaptchaRegistrationBackend', # para v0.8
        'form_class':RecaptchaRegistrationForm
    }),
    url(r'^user/', include('registration.urls')),
    
    url(r'^account/$', 'billing.views.index'),
    url(r'^pricing/$', 'billing.views.pricing'),

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

    url(r'^dynamic/$', 'dynhost.views.domains.index'),
    url(r'^dynamic/(?P<page_id>\d+)/$', 'dynhost.views.domains.index'),
    url(r'^dynamic/(?P<dom_id>\d+)/edit/$', 'dynhost.views.domains.edit'),
    url(r'^dynamic/(?P<dom_id>\d+)/delete/$', 'dynhost.views.domains.delete'),
    url(r'^dynamic/new/$', 'dynhost.views.domains.new'),
    url(r'^dynamic/help/$', direct_to_template, {
        'template': 'dynhost_help.html'
    }),

    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'index.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^404/$', 'django.views.defaults.page_not_found'),
        (r'^500/$', 'django.views.defaults.server_error'),
        (r'^media/', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT} ),
    )
