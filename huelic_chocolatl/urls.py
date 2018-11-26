"""huelic_chocolatl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout_then_login
from django.http import HttpResponse
from huelic_chocolatl import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('casa/', views.home, name="casa"),
    path('home/', views.home, name="home"),
    path('contabilidad_general/', include(('apps.contabilidad_general.urls', 'contabilidad_general'), namespace='contabilidad_general')),
    path('transaccion/', include(('apps.transaccion.urls', 'transaccion'), namespace='transaccion')),
    path('prueba/', views.prueba_logout, name="prueba"),
    path('accounts/login/', login, {'template_name':'login/login.html'}, name='login'),
    path('logout/', logout_then_login, name='logout'),

    #path('prueba/', views.prueba, name='prueba'),

    #url contabilidad_costos
    path('contabilidad_costos/',include('apps.contabilidad_costos.urls')),
    path('periodo_contable/',include('apps.periodo.urls')),

]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)