from drf_yasg.views import get_schema_view
from django.urls import path, include
from drf_yasg import openapi
from rest_framework import permissions
from movies.api.v1 import views

schema_view = get_schema_view(
    openapi.Info(
        title="Cinema Admin",
        default_version='v1',
        description="Задание выполнено на Django Rest Framework",
        contact=openapi.Contact(url=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('movies/', views.MoviesListApi.as_view()),
    path('movies/<uuid:pk>/', views.MoviesDetailApi.as_view()),
]