"""
WSGI config for educational project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys

sys.path.insert(0, '/datadisk/Home/Computing/Bioinformatics/Django/educational')
import settings
import django.core.management
import django.core.handlers.wsgi

from django.core.wsgi import get_wsgi_application

management.setup_environ(settings)
utility = management.ManagementUtility()
command = utility.fetch_command('runserver')

command.validate()

import django.conf
import django.utils
utils.translation.activate(conf.settings.LANGUAGE_CODE)



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educational.settings')

application = wsgi.WSGIHandler()
