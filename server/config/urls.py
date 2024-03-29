from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

from apps.api.routers import router

from .swagger_config import urlpatterns as swagger_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/token', obtain_auth_token, name='tokens'),
]

urlpatterns += swagger_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar

    urlpatterns += [
          path('__debug__/', include(debug_toolbar.urls)),
    ]
