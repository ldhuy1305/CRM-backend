"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from api import settings

schema_view = get_schema_view(
    openapi.Info(
        title="CRM API Documents",
        default_version="v1",
    ),
    public=True,
)

schema_api_docs = []
if settings.DEBUG:
    schema_api_docs = [
        path(
            "",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="Schema Swagger UI",
        ),
    ]
ver = settings.VERSION_REG
urlpatterns = (
    [
        path("admin/", admin.site.urls),
        re_path(f"api/{ver}/auth/", include("authentication.urls")),
        re_path(f"api/{ver}/group/", include("group.urls")),
        re_path(f"api/{ver}/users/", include("authentication.user_urls")),
        re_path(f"api/{ver}/leads/", include("lead.urls")),
        re_path(f"api/{ver}/contacts/", include("contact.urls")),
        re_path(f"api/{ver}/accounts/", include("account.urls")),
        # re_path(
        #     f"api/{ver}/notification/",
        #     include("django_notification.api.routers.notification"),
        # ),
    ]
    + staticfiles_urlpatterns()
    + schema_api_docs
)
