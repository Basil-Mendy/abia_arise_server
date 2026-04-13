"""
WSGI config for abia_arise project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abia_arise.settings')

application = get_wsgi_application()
