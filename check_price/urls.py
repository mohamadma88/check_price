
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
    path('api/price/', include('price.urls')),
    path('api/wallet/', include('wallet.urls')),
]
