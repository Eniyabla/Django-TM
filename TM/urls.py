"""turmek URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
import django
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "TURMEK ADMIN PANEL"
admin.site.title = "TURMEK | ADMIN PANEL"
import home
from home import views
from home import views
from user import views as userViews
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('selectLanguage', views.selectLanguage, name='selectLanguage'),
    path('i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += i18n_patterns(

    path(_('admin/'), admin.site.urls),
    path(_('user/'), include('user.urls')),
    path('home/', include('home.urls')),

    path('', include('home.urls')),
    path(_('about/'), views.about, name='aboutus'),
    path(_('faq/'), views.faq, name='faq'),
    path(_('contact/'), views.contact, name='contactus'),
    path(_('references/'), views.references, name='references'),
    path(_('place/'), include('place.urls')),
    path(_('search/'), views.search, name='search'),
    path('place/<int:id>/<slug:slug>', views.place_detail, name='place_detail'),
    path('category/<int:id>/<slug:slug>', views.category_places, name='category_places'),

    path('login/', userViews.loginForm, name='loginForm'),
    path('register/', userViews.signUpForm, name='signUpForm'),
    path('logout/', userViews.logoutF, name='logoutF'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    prefix_default_language=False,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
