from __future__ import unicode_literals

#--- Django
ENV = 'development'
# ENV = 'production'
# ENV = 'docker'
# DEBUG = True
# RAISE_EXCEPTIONS = True
# SECRET_KEY = 'must be declared here !!!'
# SITE_BASE_URL = ''

#--- Log files permission fix
import os
os.umask(0o002)

#--- Sentry
# SENTRY_ENABLED = False
# SENTRY_DSN = ''

#--- Admin Panel Restrictions
# RESTRICT_ADMIN = True
# ALLOWED_ADMIN_IPS = ['127.0.0.1', '::1']
# ALLOWED_ADMIN_IP_RANGES = ['127.0.0.0/24', '::/1']
# RESTRICTED_APP_NAMES = ['admin']
# TRUST_PRIVATE_IP = True
