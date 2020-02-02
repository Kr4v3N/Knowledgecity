from django.urls import path
from . import views


urlpatterns = [
    path('panel/manager/list', views.manager_list, name='manager_list'),
    path('panel/manager/group', views.manager_group, name='manager_group'),
    path('panel/manager/group/add', views.manager_group_add, name='manager_group_add'),
    path('panel/manager/group/del/<str:name>', views.manager_group_delete, name='manager_group_delete'),
    path('panel/manager/del/<int:pk>', views.manager_delete, name='manager_delete'),
]

