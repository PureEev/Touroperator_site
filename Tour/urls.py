"""
URL configuration for Tour project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Toursite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('Туры', views.tour, name ='tour'),
    path('Поиск/', views.search, name='search'),
    path('tour/', views.tour, name='tour'),
    path('buy_tour/', views.buy_tour, name = 'buy_tour'),
    path('buy_ticket/', views.buy_ticket, name = 'buy_ticket'),
    path('Возврат', views.refund, name = 'refund'),
    path('refund_action/', views.refund_action, name = 'refund_action'),
    path('statistic/', views.statistic, name = 'statistic')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)