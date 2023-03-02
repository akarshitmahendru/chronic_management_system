"""chronic_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path as url
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include


schema_view = get_schema_view(
   openapi.Info(
      title="Chronic Tool Endpoint",
      default_version='v1',
      description="Chronic Tool Endpoint Description",
      contact=openapi.Contact(email="akarshit.mahendru@doctustech.com"),
   ),
   public=True
)

urlpatterns = [
    # url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    url(r'^api/v1/', include('accounts.urls')),
    url(r'^api/v1/', include('disease_management.urls')),
    url(r'^api/v1/', include('notifications.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
