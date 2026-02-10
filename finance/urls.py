from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# URL patterns without language prefix
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Til o'zgartirish uchun
]

# URL patterns with language prefix
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('wallets/', include('wallets.urls')),
    path('categories/', include('categories.urls')),
    path('transactions/', include('transactions.urls')),
    path('transfers/', include('transfers.urls')),
    path('chat/', include('chat.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
