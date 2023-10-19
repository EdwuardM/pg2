from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Apps.authentication.urls')),
    path('products/', include('Apps.products.urls')),
    path('customers/', include('Apps.customers.urls')),
    path('suppliers/', include('Apps.suppliers.urls')),
    path('sales/', include('Apps.sales.urls')),
    path('buys/', include('Apps.buys.urls')),
    path('', include('Apps.pos.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)