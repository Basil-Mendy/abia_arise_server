"""
ASGI config for abia_arise project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abia_arise.settings')

application = get_asgi_application()
