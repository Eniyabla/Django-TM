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
from django.views.static import serve

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

    path(_('administrateur/'), admin.site.urls),
    path(_('utilisateur/'), include('user.urls')),
    path('accueil/', include('home.urls')),

    path('', include('home.urls')),
    path(_('apropos/'), views.about, name='aboutus'),
    path(_('quest-freq-posee/'), views.faq, name='faq'),
    path(_('contactez-nous/'), views.contact, name='contactus'),
    path(_('références/'), views.references, name='references'),
    path(_('produit/'), include('place.urls')),
    path(_('rechercer/'), views.search, name='search'),
    path(_('produit/<int:id>/<slug:slug>'), views.place_detail, name='place_detail'),
    path(_('categorie/<int:id>/<slug:slug>'), views.category_places, name='category_places'),

    path(_('login/'), userViews.loginForm, name='loginForm'),
    path(_('register/'), userViews.signUpForm, name='signUpForm'),
    path(_('logout/'), userViews.logoutF, name='logoutF'),

    path('ckeditor/', include('ckeditor_uploader.urls')),


    path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    prefix_default_language=False,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
