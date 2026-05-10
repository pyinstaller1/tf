from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kospi/', views.partial_kospi, name='_partial_kospi'),   # 종목 리스트만
    path('detail/', views.partial_detail, name='_partial_detail'),
    path('account/', views.account_view, name='account'),
    path('start_kospi/', views.start_kospi, name='start_kospi'),
    path('start_kospi_1day/', views.start_kospi_1day, name='start_kospi_1day'),
    path('get_ilbong_total/', views.get_ilbong_total_view, name='get_ilbong_total'),
    path('get_ilbong_1day/', views.get_ilbong_1day_view, name='get_ilbong_1day'),





    path('add_gwansim_group/', views.add_gwansim_group_view, name='add_gwansim_group'),
    path('add_gwansim_stock/', views.add_gwansim_stock_view, name='add_gwansim_stock'),
    path('get_gwansim_stock/', views.get_gwansim_stock_view, name='get_gwansim_stock'),
    



























    path('gwansim/', views.gwansim_view, name='gwansim'),

    
]








