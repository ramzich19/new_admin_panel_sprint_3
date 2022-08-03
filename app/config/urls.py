from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('debug/', include('debug_toolbar.urls')),
    path('api/', include('movies.api.urls')),

]
