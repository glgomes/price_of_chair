import os

__author__ = 'glgs'

DEBUG = False
ADMINS = frozenset([os.environ.get('ADMIN_EMAIL')])

DOMAIN = os.environ.get('DOMAIN_NAME')
