from django.contrib import admin
from django.urls import include, path

from luaas.views import list_accounts, get_flag, home

urlpatterns = [
    path('', home, name='home'),
    path('list_accounts/', list_accounts, name='list_accounts'),
    path('get_flag/', get_flag, name='get_flag')
]

handler404 = 'luaas.views.my_custom_page_not_found_view'
