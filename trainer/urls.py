"""
URL configuration for trainer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

from trainer import views

admin.autodiscover()
admin.site.site_header = _('Vocabulary Trainer')
admin.site.login = secure_admin_login(admin.site.login)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path('accounts/signup/', RedirectView.as_view(url='/', permanent=True)),
    path('accounts/', include('allauth.urls')),
    path('userprofile/', include('userprofile.urls')),
    path('word/', include('word.urls')),
    path('', views.index, name='home'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon/favicon.ico')),
]
if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
