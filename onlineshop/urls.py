from django.contrib import admin
from django.urls import path,include
from. import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',include('store.urls')),
    path('signup/', include('store.urls')), 
    path('accounts/login/', include('store.urls')),
    path('search/', include('store.urls')),
   # path('profile/', include('store.urls')),
    path('account/', include('store.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
