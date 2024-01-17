from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
	path('menu-items/', views.MenuItemsView.as_view()),
	path('groups/manager/users/', views.ManagerUserGroupView.as_view()),
	path('groups/delivery-crew/users/', views.DeliveryCrewUserGroupView.as_view()),
	path('token/login/', obtain_auth_token),
]
