from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')), # подключение URL-ов приложения catalog
    path('blog/', include('blog.urls')), # подключение URL-ов приложения blog
    path('accounts/', include('accounts.urls')), # подключение URL-ов приложения accounts
]

# Обслуживание медиафайлов при DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
