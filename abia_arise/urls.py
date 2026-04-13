"""
URL configuration for abia_arise project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from core.views import SendEmailView

# Simple API root view
class APIRootView(View):
    def get(self, request):
        return JsonResponse({
            'message': 'Welcome to Abia Arise API',
            'endpoints': {
                'admin': '/admin/',
                'api_auth': '/api/auth/',
                'api_core': '/api/core/',
                'api_messaging': '/api/messaging/',
            }
        })

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/core/', include('core.urls')),
    path('api/messaging/send-email/', SendEmailView.as_view(), name='send-email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
