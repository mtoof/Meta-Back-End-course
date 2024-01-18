from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import MenuItemsSerializer, UserSerializer
from .models import MenuItem
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from django.http import Http404
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from rest_framework.validators import ValidationError

class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user.groups.filter(name='admin').exists() or user.groups.filter(name='manager').exists()
        return False

class IsManagerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Manager').exists():
            return True
        return False

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SingleItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]




# Only managers can add users to manager or delivery-crew #
# Only acceptable groups are manager or delivery-crew 
class BaseUserGroupView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagerOnly]
    def get_group(self):
        group_name = self.kwargs['group_name']
        if group_name == 'manager':
            return Group.objects.get(name='Manager')
        elif group_name == 'delivery-crew':
            return Group.objects.get(name='Delivery crew')
        else:
            raise NotFound("Group not found")

    def get_user(self, username):
       if not username:
           raise ValidationError('Username is required')
       return get_object_or_404(User, username=username)

    def get_user_id(self, id):
        if not id:
            raise ValidationError('ID is required')
        return get_object_or_404(User, id=id)

class UserGroupView(BaseUserGroupView):
    def get(self, request, *args, **kwargs):
        group = self.get_group()
        users = User.objects.filter(groups=group)
        seializer = self.serializer_class(users, many=True)
        return Response(seializer.data)
    def post(self, request, *args, **kwargs):
        group = self.get_group()
        user = self.get_user(request.data.get('username'))
        if group not in user.groups.all():
            user.groups.add(group)
            user.save()
            return Response({'message': f'User added to the {group.name} group'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': f'User "{user.username}" is already in the "{group.name}" group'}, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserGroupView(BaseUserGroupView):
    def delete(self, request, *args, **kwargs):
        group = self.get_group()
        user = self.get_user_id(kwargs.get('id'))
        if group in user.groups.all():
            user.groups.remove(group)
            user.save()
            return Response({'message': f'User removed from the {group.name} group'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': f'User "{user.username}" is not in the "{group.name}" group'}, status=status.HTTP_400_BAD_REQUEST)