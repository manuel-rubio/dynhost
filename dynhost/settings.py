# -*- coding: utf-8 -*-
# Django settings for dynhost project.
from os.path import dirname, abspath
from os import makedirs
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Manuel Rubio', 'bombadil@bosqueviejo.net'),
)

## TODO: add .it and .fr when we have support for them
TLD_GRANTED = (
    '.com.es', '.org.es', '.nom.es', '.pl', '.co.uk', '.me.uk',
    '.org.uk', '.es', '.de', '.be', '.com', '.eu', '.in', '.info',
    '.name', '.net', '.nl', '.pm', '.re', '.tel', '.tf', '.us',
    '.wf', '.yt', '.biz', '.org', '.ca', '.at', '.ch', '.cn', '.cz',
    '.li', '.tn', '.asia', '.dk', '.mobi', '.pro', '.se', '.so'
)

BANK = 'ING Direct'
CCC = '1465 0100 92 6000285598'

COMPANY_NAME = u'Altenwald Solutions, S.L.'
COMPANY_ID = u'ESB14985659'
COMPANY_ADDR = u'Calle La Fragua, 7'
COMPANY_ZIP = u'14100'
COMPANY_CITY = u'La Carlota'
COMPANY_STATE = u'Córdoba'
COMPANY_COUNTRY = u'España'
COMPANY_PHONE = u'+34651108590'
COMPANY_WEB = u'http://altenwald.com'
COMPANY_EMAIL = u'info@altenwald.com'
COMPANY_LOGO = '/var/www/dynhost/static/img/dynhost_logo.png'

DOMAIN_PRICE = 12.0

PLUS_MAIL_QTY = 10
PLUS_MAIL_PRICE = 0.1

PREMIUM_MAIL_QTY = 10
PREMIUM_MAIL_PRICE = 0.3

REDIRECT_MAIL_QTY = 100
REDIRECT_MAIL_PRICE = 0.01

MYSQL_DB_PRICE = 3.0

PROJECT_PATH = abspath(dirname(abspath(__file__)) + "/..")

OVH_USER = ''
OVH_PASS = ''
DOMAIN_CONTACT = ''
OVH_USERS_PASS = ''
DNS_CONFIG = (
    'ns1.bosqueviejo.net',
    'ns2.bosqueviejo.net',
    'ns3.bosqueviejo.net',
    'ns4.bosqueviejo.net'
)

IVA = 'ESB14985659'

WSDL_FILE = PROJECT_PATH + "/ovh/soapi-re-1.61.wsdl"
# WSDL = 'https://www.ovh.com/soapi/soapi-re-1.61.wsdl'

DEFAULT_IP = '176.31.105.29'

RECAPTCHA_PUBLIC_KEY = '6LdpP88SAAAAAHYByZgLpgN4RDzAuaLs3vwTD3uL'
RECAPTCHA_PRIVATE_KEY = '6LdpP88SAAAAAMy9payK06HWlpTGQbQ6ErWao7Ez'
RECAPTCHA_USE_SSL = True

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ring2',                      # Or path to database file if using sqlite3.
        'USER': 'ring',                      # Not used with sqlite3.
        'PASSWORD': 'ring1234',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/dynhost.sqlite'
    }

USER_SKEL = {
    'dynhost': 'apache/conf.d/dynhosts/%(userid)d',
    'redirect': 'apache/conf.d/redirects/%(userid)d',
    'hosting': 'apache/conf.d/hostings/%(userid)d',
    'base': 'apache/conf.d/base/%(userid)d',
    'www-data': '%(userid)d/www-data',
    'logs': 'apache/%(userid)d/log',
    'ftp': 'ftp',
}
REAL_USER_SKEL = {
    'dynhost': 'apache/conf.d/dynhosts',
    'redirect': 'apache/conf.d/redirects',
    'hosting': 'apache/conf.d/hostings',
    'base': 'apache/conf.d/base',
    'www-data': 'www-data',
    'logs': 'apache/log',
    'ftp': 'ftp',
}
HOMEDIR_BASE = '/home/dynhost'

if 'test' in sys.argv:
    import shutil
    HOMEDIR_BASE = '/tmp/dynhost'
    shutil.rmtree("/tmp/dynhost", True)
    makedirs("/tmp/dynhost")
    
MARIADB_HOST = 'localhost'
MARIADB_USER = 'root'
MARIADB_PASS = ''

MARIADB_CREATE_USER = """
CREATE USER '%(user)s'@'localhost' IDENTIFIED BY '%(pass)s';
"""

MARIADB_REMOVE_USER = """
DROP USER '%(user)s'@'localhost';
"""

MARIADB_LINK_USER = """
GRANT ALL ON `%(name)s`.* TO '%(user)s'@'localhost';
"""

MARIADB_UNLINK_USER = """
REVOKE ALL ON `%(name)s`.* FROM '%(user)s'@'localhost';
"""

MARIADB_CREATE_DB = """
CREATE DATABASE `%(name)s`;
"""

MARIADB_REMOVE_DB = """
DROP DATABASE `%(name)s`;
"""

MARIADB_CHANGE_USER = """
RENAME USER '%(old)s'@'localhost' TO '%(user)s'@'localhost';
"""

MARIADB_CHANGE_PASS = """
SET PASSWORD FOR '%(user)s'@'localhost' = PASSWORD('%(pass)s');
"""

PROFTPD_RELOAD_CMD = 'ls' #'sudo /etc/init.d/proftpd reload'
PROFTPD_CONFIG_BASE = """
<Directory ~%(user)s>
        <Limit ALL>
                Order Allow,Deny
                AllowUser %(user)s
                Deny ALL
        </Limit>
</Directory>

"""

APACHE_RELOAD_CMD = 'ls' #'sudo /etc/init.d/apache2 reload'
APACHE_BASE = """
<VirtualHost *:80>
    ServerAdmin %(email)s
    ServerName %(name)s

    <IfModule mpm_itk_module>
        AssignUserId #%(uid)s #1003
    </IfModule>

    Include %%(dyndir)s/*.%(name)s
    Include %%(reddir)s/*.%(name)s
    Include %%(hosdir)s/*.%(name)s

    DocumentRoot %(path)s
    <Directory />
        Options SymLinksIfOwnerMatch
        AllowOverride None
        Order deny,allow
        deny from all
    </Directory>
    <Directory %(path)s>
        Options %(options)s
        AllowOverride None
        Order allow,deny
        allow from all
    </Directory>

    LogLevel warn
    ErrorLog %%(logdir)s/%(name)s.error.log
    CustomLog %%(logdir)s/%(name)s.access.log combined
    ServerSignature Off
</VirtualHost>

"""
APACHE_REDIRECT_PART = """
ProxyPass  %(uri)s %(url)s

"""
APACHE_HOSTING_PART = """
Alias %(uri)s %(path)s
<Directory %(path)s>
    Options %(options)s
    AllowOverride AuthConfig Indexes Limit
    Order deny,allow
    Allow from all
    php_admin_value open_base %(path)s
</Directory>

"""

AUTH_PROFILE_MODULE = 'billing.Accounts'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/bombadil/www-data/dynhost.es/htdocs/static'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH + '/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%6sy_bhgqn!*0j_-n*js43v8^dckrpc1*gziduvka%xd($x$qi'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.FailedLoginMiddleware',
)

ROOT_URLCONF = 'dynhost.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dynhost.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH + '/dynamic/templates',
    PROJECT_PATH + '/billing/templates',
    PROJECT_PATH + '/dns/templates',
    PROJECT_PATH + '/database/templates',
    PROJECT_PATH + '/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    'registration',
    'captcha',
    'gravatar',
    'axes',
    'django_extensions',
    # project apps:
    'billing',
    'ftp',
    'dns',
    'dynamic',
    'mail',
    'database',
    'web',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'noreply@dynhost.es'
LOGIN_REDIRECT_URL = '/'

GRAVATAR_DEFAULT_IMAGE = 'mm'
GRAVATAR_DEFAULT_RATING = 'g'
GRAVATAR_DEFAULT_SIZE = 32

AXES_LOGIN_FAILURE_LIMIT = 5
AXES_LOCK_OUT_AT_FAILURE = True
AXES_USE_USER_AGENT = False
AXES_COOLOFF_TIME = 6 # hours to forgot malicious IPs
AXES_LOGGER = 'axes.watch_login'
AXES_LOCKOUT_TEMPLATE = 'lockout.html'
AXES_LOCKOUT_URL = None
AXES_VERBOSE = True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
