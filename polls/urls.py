from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('apc/', views.apcalc, name='apc'),
    path('graph_ap/', views.graph_ap, name='graph_ap'),
    path('graph_hp/', views.graph_hp, name='graph_hp'),
    path('graph_mp/', views.graph_mp, name='graph_mp'),
    path('graph_all/', views.graph_all, name='graph_all'),
    path('analysis/plot/', views.img_plot, name="img_plot"),
]
