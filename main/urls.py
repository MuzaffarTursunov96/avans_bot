
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [ 
path('user-list',views.ListUsers.as_view(),name='user_list'),
path('user-create',views.CreateAvansUserView.as_view(),name='user_create'),
path('get-user-ids',views.UserIds.as_view(),name='get_user_ids'),
path('update-user/<int:id>',views.UserUpdate.as_view(),name='update_user'),
path('user-delete',views.UserDelete.as_view(),name='delete_user'),
path('user-avans-save',views.UserAvansSave.as_view(),name='user_avans_save'),
path('user-avans-check',views.UserAvansCheck.as_view(),name='user_avans_check'),
path('get-users-for-message',views.GetUsersForMessage.as_view(),name='get_users_for_message'),
path('get-path-excell',views.GetPathExcel.as_view(),name='get_path_excell'),
]
