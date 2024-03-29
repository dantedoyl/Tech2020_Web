"""askTorzhkov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from app import views
from django.conf.urls import url
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hot/', views.hot, name='hot'),
    path('', views.index, name='index'),
    path('tag/<slug:tag>/', views.tag, name='tag'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('registr/', views.registr, name='registr'),
    path('question/<int:id>/', views.question, name='question'),
    path('/', views.logout, name='logout'),
    path('vote/', views.vote, name='vote'),
    path('correct/', views.correct, name='correct'),
    url('', include('django_prometheus.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)