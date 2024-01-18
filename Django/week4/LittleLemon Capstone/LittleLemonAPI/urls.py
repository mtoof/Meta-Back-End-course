from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
	path('menu-items/', views.MenuItemsView.as_view()),
	path('groups/<str:group_name>/users/', views.UserGroupView.as_view()),
	path('groups/<str:group_name>/users/<int:id>', views.DeleteUserGroupView.as_view()),
	path('token/login/', obtain_auth_token),
]
