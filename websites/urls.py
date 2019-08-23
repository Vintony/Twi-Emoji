"""website URL Configuration

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
from django.urls import include, path
from . import views, search_crawler

urlpatterns = [
    path('index/', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('search_crawler_page', views.search_crawler_page, name='search_crawler_page'),
    path('user_crawler_page', views.user_crawler_page, name='user_crawler_page'),
    path('stream_crawler_page', views.stream_crawler_page, name='stream_crawler_page'),
    path('accounts_type_definer_page', views.accounts_type_definer_page, name='accounts_type_definer_page'),
    path('report_page', views.report_page, name='report_page'),
    path('data_export_page', views.data_export_page, name='data_export_page'),
]
